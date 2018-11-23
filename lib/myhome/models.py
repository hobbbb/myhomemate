
from jsonfield import JSONField

from django.contrib.auth.models import User
from django.db import models


# class Room(models.Model):
#     name = models.CharField(max_length=50)


class Zone(models.Model):
    name = models.CharField(max_length=50)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    radius = models.PositiveSmallIntegerField()


class Component(models.Model):
    uniq_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=0)
    data = JSONField()

    def __str__(self):
        return self.name


class Device(models.Model):
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


class Entity(models.Model):
    name = models.CharField(max_length=200, unique=True)


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
