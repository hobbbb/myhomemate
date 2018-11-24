import time

from jsonfield import JSONField

from django.contrib.auth.models import User
from django.db import models


class Device(models.Model):
    last_saved = None

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    component = models.ForeignKey('myhome.Component', on_delete=models.CASCADE)
    uniq_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    battery = models.PositiveSmallIntegerField(null=True)
    data = JSONField()
    is_tracking = models.BooleanField(default=0)

    def __str__(self):
        return self.name
