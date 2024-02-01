from typing import Optional

from django.conf import settings
from django.urls import reverse

from diag_report.models import DiagReport, BatteryHealth
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
                LegendTitleRow(title="اقای‌اندروید", subtitle="کارشناسی‌آنلاین", has_divider=True),
                DescriptionRow(text="با کارشناسی‌آنلاین اندروید مشخصات دقیق آگهی را بدست آورید و مطمئن تر خرید کنید",
                               has_divider=True),
                ScoreRow(title="ورژن اندروید",
                         descriptive_score=f"{report.os_version}{get_android_name(report.os_version)}",
                         score_color=Color.SUCCESS_PRIMARY,
                         has_divider=True,
                         icon=Icon(icon_name=IconName.SETTINGS)),
                ScoreRow(title="برند برد", descriptive_score=f"{report.device_board}",
                         icon=Icon(icon_name=IconName.SETTINGS)),
                ScoreRow(title="برند پردازنده", descriptive_score=f"{report.device_hardware}",
                         icon=Icon(icon_name=IconName.SETTINGS)),
                ScoreRow(title="وضعیت باتری", descriptive_score=get_battery_descriptive(report.battery),
                         score_color=get_battery_color(report.battery), icon=Icon(icon_name=IconName.SETTINGS)),
                ScoreRow(title="مقدار رم", descriptive_score=f"{round(float(report.total_memory) / 1e9)}",
                         icon=Icon(icon_name=IconName.SETTINGS)),
                ScoreRow(title="مدل نامبر", descriptive_score=report.device_model,
                         icon=Icon(icon_name=IconName.SETTINGS)),
                WideButtonBar(
                    button=Button(
                        title="اطلاعات بیشتر",
                        action=Action(
                            action_type=ActionType.LOAD_WEB_VIEW_PAGE,
                            fallback_link=settings.HOST + reverse(
                                "diag:view-report", kwargs={"report_id": report.id}
                            )
                        )
                    ),
                    style=Style.SECONDARY,
                )
            ]
        ),
        settings.API_KEY,
        access_token
    )


def get_battery_descriptive(battery: BatteryHealth) -> str:
    if battery.value == BatteryHealth.GOOD:
        return "خوب"
    if battery.value == BatteryHealth.COLD:
        return "سرد"
    if battery.value == BatteryHealth.DEAD:
        return "نیاز به تعویض"
    if battery.value == BatteryHealth.OVER_VOLTAGE:
        return "ولتاژ بیش‌از‌حد"
    if battery.value == BatteryHealth.OVERHEAT:
        return "داغ‌‌شدگی"
    return "نامشخص"


def get_battery_color(battery: BatteryHealth) -> Color:
    if battery.value == BatteryHealth.GOOD:
        return Color.SUCCESS_PRIMARY
    if battery.value == BatteryHealth.UNKNOWN:
        return Color.TEXT_PRIMARY
    return Color.ERROR_PRIMARY


def get_phone_image(report: DiagReport) -> Optional[str]:
    _search_params = {
        'q': f"phone {report.device_brand} {report.device_model}",
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


def get_format_by_content_type(content_type):
    MIME_TYPE_MAPPING = {
        'audio/mpeg': '.mp3',
        'audio/ogg': '.ogg',
        'audio/wav': '.wav',
        'audio/x-wav': '.wav',
        'audio/webm': '.webm',
        'audio/aac': '.aac',
        'audio/mp4': '.mp4',  # or .m4a for audio-only MP4 container
        'audio/flac': '.flac',
        'audio/x-flac': '.flac',
        'audio/x-aiff': '.aiff',
        'audio/vnd.wav': '.wav',
        'audio/3gpp': '.3gp',
        'audio/3gpp2': '.3g2',
        'video/mp4': '.mp4',
        'video/mpeg': '.mpeg',
        'video/ogg': '.ogv',
        'video/webm': '.webm',
        'video/3gpp': '.3gp',
        'video/3gpp2': '.3g2',
        'video/x-msvideo': '.avi',
        'video/x-ms-wmv': '.wmv',
        'video/x-flv': '.flv',
        'video/x-matroska': '.mkv',
        'image/jpeg': '.jpg',
        'image/png': '.png',
        'image/gif': '.gif',
        'image/webp': '.webp',
        'image/tiff': '.tiff',
        'image/x-icon': '.ico',
        'image/svg+xml': '.svg',
        'image/bmp': '.bmp',
        'text/plain': '.txt',
        'text/html': '.html',
        'text/css': '.css',
        'text/csv': '.csv',
        'text/javascript': '.js',
        'application/json': '.json',
        'application/ld+json': '.jsonld',
        'application/xml': '.xml',
        'application/zip': '.zip',
        'application/x-7z-compressed': '.7z',
        'application/x-rar-compressed': '.rar',
        'application/pdf': '.pdf',
        'application/msword': '.doc',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx',
        'application/vnd.ms-excel': '.xls',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': '.xlsx',
        'application/vnd.ms-powerpoint': '.ppt',
        'application/vnd.openxmlformats-officedocument.presentationml.presentation': '.pptx',
    }
    return MIME_TYPE_MAPPING.get(content_type, "")
