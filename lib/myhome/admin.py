from django.contrib import admin

from myhome.models import Room, Device, Component


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    pass


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    pass


@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    pass
