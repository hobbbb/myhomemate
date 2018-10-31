
import json

from django.contrib.auth.models import User
from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=50)


class Device(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=50)


class Component(models.Model):
    name = models.CharField(max_length=50, unique=True)
    data_raw = models.TextField(db_column='data')

    def __str__(self):
        return self.name

    @property
    def data(self):
        if not self.data_raw:
            return
        return json.loads(self.data_raw)
