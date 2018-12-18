import math
from jsonfield import JSONField

from django.contrib.auth.models import User
from django.db import models


class Component(models.Model):
    uniq_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=0)
    data = JSONField()

    def __str__(self):
        return self.name


class Device(models.Model):
    zone = None

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    uniq_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    battery = models.PositiveSmallIntegerField(null=True)
    data = JSONField()
    is_tracking = models.BooleanField(default=0)

    def __str__(self):
        return self.name

    @property
    def is_tracker(self):
        if not (self.latitude and self.longitude):
            return False
        return True


class Zone(models.Model):
    name = models.CharField(max_length=50)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    radius = models.PositiveSmallIntegerField()

    def verification(self, mlat, mlon, acc=50):
        earth_radius = 6371
        slat = float(self.latitude)
        slon = float(self.longitude)
        dlat = math.radians(mlat - slat)
        dlon = math.radians(mlon - slon)
        slat = math.radians(slat)
        mlat = math.radians(mlat)

        a = math.sin(dlat / 2) ** 2 + (math.sin(dlon / 2) ** 2) * math.cos(slat) * math.cos(mlat)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        dist = earth_radius * c * 1000

        if dist < self.radius + acc:
            return True
        else:
            return False


class Entity(models.Model):
    name = models.CharField(max_length=200, unique=True)


# class Room(models.Model):
#     name = models.CharField(max_length=50)


class Script(models.Model):
    name = models.CharField(max_length=200, unique=True)
    text = models.TextField()


# class Automation(models.Model):
#     name = models.CharField(max_length=100)
#     trigger = models.ForeignKey(AutomationTrigger, on_delete=models.CASCADE)
#     # condition = models.ForeignKey(AutomationCondition, on_delete=models.CASCADE, null=True)
#     action = models.ForeignKey(AutomationAction, on_delete=models.CASCADE)
