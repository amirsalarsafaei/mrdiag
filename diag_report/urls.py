"""
URL configuration for kenar_sample_addon project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from diag_report.views import *
urlpatterns = [
    path("start/", start, name="start"),
    path("landing/", landing, name="landing"),
    path("begin_diag/", begin_diag, name="begin-diag"),
    path("create-report/", create_report, name="create-report"),
    path("submit-report/", submit_report, name="submit-report"),
    path('upload/', upload_file, name='file-upload-api'),
    path('view-report/<int:report_id>/', view_report, name='view-report'),
]

app_name = 'diag_report'
