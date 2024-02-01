import logging

from django.core.files.base import ContentFile
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404 as get_object_or_404_django
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework.views import APIView

from kenar.utils.errors import DivarException
from oauth import controller as oauth_controller

from rest_framework import generics, status

from .models import DiagReport, File
from .serializers import DiagReportSerializer, SubmitDiagReportSerializer, FileSerializer
from .controller import get_phone_image, create_report_addon, get_format_by_content_type

logger = logging.getLogger(__name__)


@api_view(['POST'])
@transaction.atomic
def create_report(request, *args, **kwargs):
    serializer = DiagReportSerializer(data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    report: DiagReport = serializer.save()
    report.image = get_phone_image(report)
    report.ticket.used = True
    report.save()

    serializer = DiagReportSerializer(report, context={'request': request})
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def submit_report(request, *args, **kwargs):
    serializer = SubmitDiagReportSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    report = get_object_or_404(DiagReport, ticket_id=serializer.validated_data['ticket'])
    try:
        create_report_addon(report)
        report.submitted = True
        report.save()
    except DivarException as e:
        logger.error("could not create addon", e.message)
        raise APIException("could not create addon")
    except Exception as e:
        logger.error("could not create addon", type(e))
        raise APIException("could not create addon")

    return Response({"deep_link": f"https://divar.ir/v/{report.ticket.oauth.approved_addon_token()}"},
                    status=status.HTTP_200_OK)


def landing(request):
    token = request.GET.get("post_token")
    if token is None:
        return render(
            request,
            "error.html"
        )

    return render(
        request,
        'diag_report/landing.html',
        {
            "token": token,
        }
    )


def start(request):
    token = request.GET.get("token")
    if token is None:
        return render(
            request,
            "error.html"
        )

    oauth_url = oauth_controller.create_redirect_link(
        request=request,
        scopes=(oauth_controller.create_phone_scope(), oauth_controller.create_approved_addon_scope(token)),
    )

    return redirect(oauth_url)


def begin_diag(request):
    ticket = request.GET.get("ticket")
    if ticket is None:
        return render(
            request,
            "error.html",
        )

    return render(
        request,
        'diag_report/begin_diag.html',
        {
            "ticket": ticket,
        }
    )


@csrf_exempt
@transaction.atomic
def upload_file(request, *args, **kwargs):
    content_file = ContentFile(request.body)
    file = File()
    file.save()
    file.file.save(str(file.file_id) + get_format_by_content_type(request.content_type), content_file)
    file.save()
    return JsonResponse({"id": str(file.file_id)},
                        status=status.HTTP_201_CREATED)


def view_report(request, report_id):
    report = get_object_or_404_django(DiagReport, id=report_id)
    serializer = DiagReportSerializer(report, context={'request': request})
    return render(
        request,
        'diag_report/view_report.html',
        {
            "report": serializer.data,
        }
    )