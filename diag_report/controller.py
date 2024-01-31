from typing import Optional

from django.conf import settings

from diag_report.models import DiagReport
from google_images_search import GoogleImagesSearch

from kenar.clients.addons import addons_client
from kenar.models.addon import Addon
from kenar.models.icons import IconName
from kenar.models.widgets import *

gis = GoogleImagesSearch(settings.GOOGLE_KEY, '3171bf9de69d14b64')


def create_report_addon(report: DiagReport):
    access_token = report.ticket.oauth.access_token
    post_token = report.ticket.oauth.approved_addon_token()

    addons_client.create_post_addon(
        post_token,
        Addon(
            widgets=[
                LegendTitleRow(title="اقای‌آندروید", subtitle="کارشناسی‌آنلاین", has_divider=True),
                DescriptionRow(text="با کارشناسی‌آنلاین اندروید مشخصات دقیق آگهی را بدست آورید و مطمئن تر خرید کنید",
                               has_divider=True),
                ScoreRow(title="ورژن آندروید",
                         descriptive_score=f"{report.os_version}",
                         score_color=Color.SUCCESS_PRIMARY,
                         has_divider=True,
                         icon=Icon(icon_name=IconName.BRAND_GOOGLE)),
                ScoreRow(title="برند برد", descriptive_score=f"{report.device_board}", icon=Icon(icon_name=IconName.BRAND_GOOGLE)),
                ScoreRow(title="برند پردازنده", descriptive_score=f"{report.device_hardware}", icon=Icon(icon_name=IconName.BRAND_GOOGLE))
            ]
        ),
        settings.API_KEY,
        access_token
    )


def get_phone_image(report: DiagReport) -> Optional[str]:
    _search_params = {
        'q': report.device_model,
        'num': 1,
        'fileType': 'jpg',
        'imgSize': 'large',
    }
    gis.search(search_params=_search_params)
    if len(gis.results()) == 0:
        return None
    return gis.results()[0].url


def get_android_name(version):
    # Android version names as of the last update in early 2023
    version_names = {
        "1.5": "Cupcake",
        "1.6": "Donut",
        "2.0": "Eclair",
        "2.1": "Eclair",
        "2,2": "Froyo",
        "2.3": "Gingerbread",
        "3.0": "Honeycomb",
        "3.1": "Honeycomb",
        "3.2": "Honeycomb",
        "4.0": "Ice Cream Sandwich",
        "4.1": "Jelly Bean",
        "4.2": "Jelly Bean",
        "4.3": "Jelly Bean",
        "4.4": "KitKat",
        "5.0": "Lollipop",
        "5.1": "Lollipop",
        "6.0": "Marshmallow",
        "7.0": "Nougat",
        "7.1": "Nougat",
        "8.0": "Oreo",
        "8.1": "Oreo",
        "9": "Pie",
        "10": "Queen Cake",
        "11": "Red Velvet Cake",
        "12": "Snow Cone",
        "12.1": "Snow Cone v1.1",
        "13": "Tiramisu"
    }

    # Return the corresponding name; if not found, return "Unknown"
    return version_names.get(str(version), "Unknown")

