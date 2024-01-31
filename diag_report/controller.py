from typing import Optional

from django.conf import settings

from diag_report.models import DiagReport
from google_images_search import GoogleImagesSearch

gis = GoogleImagesSearch(settings.GOOGLE_KEY, '3171bf9de69d14b64')


def create_report_addon(report: DiagReport):
    pass


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
