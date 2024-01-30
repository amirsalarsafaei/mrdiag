from django.shortcuts import render, redirect
from oauth import controller as oauth_controller


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
        callback_view="diag:oauth-callback"
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
