
from django.contrib.auth.models import User
from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=50)


class Device(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=50)
