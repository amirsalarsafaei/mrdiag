import uuid
from enum import IntEnum

from django.db import models
from oauth.models import OAuth


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
                                      default=BatteryHealth.UNKNOWN.name)
    available_memory = models.CharField(default="0", max_length=512)
    total_memory = models.CharField(default="0", max_length=512)
    device_model = models.CharField(max_length=512, blank=True, default="")
    device_brand = models.CharField(max_length=512, blank=True, default="")
    device_board = models.CharField(max_length=512, blank=True, default="")
    device_hardware = models.CharField(max_length=512, blank=True, default="")
    device_manufacturer = models.CharField(max_length=512, blank=True, default="")
    device_product = models.CharField(max_length=512, blank=True, default="")
    os_version = models.CharField(default="0", max_length=512)

    image = models.URLField(null=True)
    submitted = models.BooleanField(default=False)