import math
from jsonfield import JSONField

from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import models


class Component(models.Model):
    uniq_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=0)
    data = JSONField()

    def __str__(self):
        return self.name


class Device(models.Model):
    last_saved = None
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

    def refresh(self, **kwargs):
        for k in ['latitude', 'longitude', 'battery']:
            setattr(self, k, kwargs.get(k))

        zones = cache.get('zones')
        for _, zn in zones.items():
            if not (self.latitude and self.longitude):
                continue

            in_zone = zn.verification(self.latitude, self.longitude)
            if in_zone is True:
                self.zone = zn.id
            print(self, ' in zone' if t else ' out of zone')

        return self


class Zone(models.Model):
    name = models.CharField(max_length=50)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    radius = models.PositiveSmallIntegerField()

    def verification(self, latitude, longitude):
        dist = self.radius / 1000
        mylat = self.latitude
        mylon = self.longitude
        lat1 = float(mylat) - dist / 111.
        lat2 = float(mylat) + dist / 111.
        lon1 = float(mylon) - dist / abs(math.cos(math.radians(mylat)) * 111.)  # 1 градус широты = 111 км
        lon2 = float(mylon) + dist / abs(math.cos(math.radians(mylat)) * 111.)

        if lat1 < latitude and latitude < lat2 and lon1 < longitude and longitude < lon2:
            return True
        else:
            return False


class Entity(models.Model):
    name = models.CharField(max_length=200, unique=True)


# class Room(models.Model):
#     name = models.CharField(max_length=50)


class Service(models.Model):
    name = models.CharField(max_length=200, unique=True)


# class AutomationTrigger(models.Model):
#     entity = models.ForeignKey(Entity, on_delete=models.CASCADE, null=True)
#     zone = models.ForeignKey(Zone, on_delete=models.CASCADE, null=True)


# class AutomationCondition(models.Model):
#     pass


# class AutomationAction(models.Model):
#     service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True)


# class Automation(models.Model):
#     name = models.CharField(max_length=100)
#     trigger = models.ForeignKey(AutomationTrigger, on_delete=models.CASCADE)
#     # condition = models.ForeignKey(AutomationCondition, on_delete=models.CASCADE, null=True)
#     action = models.ForeignKey(AutomationAction, on_delete=models.CASCADE)
