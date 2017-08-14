from __future__ import unicode_literals

from django.db import models


class Device(models.Model):
    device_id = models.CharField(max_length=100, unique=True)


class Datum(models.Model):
    time = models.DateTimeField('date published')
    device = models.ForeignKey(Device, null=False, on_delete=models.CASCADE)
    type = models.IntegerField(default=0)  # 1: sensor, 2: gateway
    status = models.IntegerField(default=0)  # 1: offline, 2: online

