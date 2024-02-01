import uuid
from enum import IntEnum

from django.db import models
from django.utils.datetime_safe import datetime

from oauth.models import OAuth


class File(models.Model):
    file_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    file = models.FileField(upload_to='uploads/')


class BatteryHealth(IntEnum):
    GOOD = 1
    OVERHEAT = 2
    DEAD = 3
    OVER_VOLTAGE = 4
    UNSPECIFIED_FAILURE = 5
    COLD = 6
    UNKNOWN = 7

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class SubmitTicket(models.Model):
    ticket = models.UUIDField(primary_key=True, default=uuid.uuid4)
    used = models.BooleanField(default=False)
    oauth = models.ForeignKey(to=OAuth, to_field='id', on_delete=models.CASCADE)


class DiagReport(models.Model):
    ticket = models.OneToOneField(to=SubmitTicket, to_field='ticket', on_delete=models.CASCADE)
    battery_health = models.CharField(max_length=100, choices=BatteryHealth.choices(),
                                      default=str(BatteryHealth.UNKNOWN.value))

    available_memory = models.BigIntegerField(default=0)
    total_memory = models.BigIntegerField(default=0)

    device_model = models.CharField(max_length=512, blank=True, default="")
    device_brand = models.CharField(max_length=512, blank=True, default="")
    device_board = models.CharField(max_length=512, blank=True, default="")
    device_hardware = models.CharField(max_length=512, blank=True, default="")
    device_manufacturer = models.CharField(max_length=512, blank=True, default="")
    device_product = models.CharField(max_length=512, blank=True, default="")
    os_version = models.CharField(default="0", max_length=512)
    total_internal_memory = models.BigIntegerField(default=0)
    camera_test = models.ForeignKey(to=File, to_field='file_id', on_delete=models.CASCADE, related_name="report_from_camera")
    mic_test = models.ForeignKey(to=File, to_field='file_id', on_delete=models.CASCADE, related_name="report_from_mic")
    is_port_healthy = models.BooleanField(default=False)

    image = models.URLField(null=True)
    submitted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def battery(self):
        return BatteryHealth(int(self.battery_health))


def format_bytes(bytes: int):
    if bytes < 2**10:
        return f"{bytes} Bytes"
    if bytes < 2**20:
        return f"{bytes // 1024} KB"
    if bytes < 2**30:
        return f"{bytes // (2**20)} MB"
    return f"{bytes // (2**30)} GB"
