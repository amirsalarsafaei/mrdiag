from django.db import models
from oauth.models import OAuth


class SubmitTicket(models.Model):
    ticket = models.UUIDField(primary_key=True)
    used = models.BooleanField(default=False)
    oauth = models.ForeignKey(to=OAuth, to_field='id', on_delete=models.CASCADE)


class DiagReport(models.Model):
    ticket = models.ForeignKey(to=SubmitTicket, to_field='ticket', on_delete=models.CASCADE)
