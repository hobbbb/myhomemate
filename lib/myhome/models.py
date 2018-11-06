
import json

from django.contrib.auth.models import User
from django.db import models


class DataJsonMixin(object):
    # TODO: fix mixin
    data_raw = models.TextField(db_column='data')

    @property
    def data(self):
        if not self.data_raw:
            return
        return json.loads(self.data_raw)

# class Room(models.Model):
#     name = models.CharField(max_length=50)


# class Zone(models.Model):
#     name = models.CharField(max_length=50)


class Component(DataJsonMixin, models.Model):
    name = models.CharField(max_length=100, unique=True)
    human_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=0)
    data_raw = models.TextField(db_column='data')

    @property
    def data(self):
        if not self.data_raw:
            return
        return json.loads(self.data_raw)

    def __str__(self):
        return self.name


class Device(DataJsonMixin, models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    human_name = models.CharField(max_length=100)
    is_tracking = models.BooleanField(default=0)
    data_raw = models.TextField(db_column='data')

    @property
    def data(self):
        if not self.data_raw:
            return
        return json.loads(self.data_raw)

    def __str__(self):
        return self.name
