import logging

from django.conf import settings
from django.db import transaction
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from kenar.clients.addons import addons_client
from kenar.models.addon import Addon
from kenar.models.colors import Color
from kenar.models.widgets import LegendTitleRow, ScoreRow
from kenar.utils.errors import DivarException
from oauth import controller as oauth_controller

from rest_framework import generics, status

from .models import DiagReport
from .serializers import DiagReportSerializer, SubmitDiagReportSerializer
from .controller import get_phone_image, create_report_addon

logger = logging.getLogger(__name__)


@api_view(['POST'])
@transaction.atomic
def create_report(request, *args, **kwargs):
    serializer = DiagReportSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    report: DiagReport = serializer.save()
    report.image = get_phone_image(report)
    report.ticket.used = True
    report.save()

    serializer = DiagReportSerializer(report)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def submit_report(request, *args, **kwargs):
    serializer = SubmitDiagReportSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    report = get_object_or_404(DiagReport, ticket=serializer.validated_data['ticket'])
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

    return Response({"deep_link": ""}, status=status.HTTP_200_OK)

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
