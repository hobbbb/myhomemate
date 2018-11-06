import inspect
import re

from myhome import models


def register_component(config):
    component_name = re.sub(r'(^lib/components/)|(/__init__.py$)', '', inspect.stack()[1][1]).replace('/', '.')
    component = models.Component.objects.filter(name=component_name).first()
    if component:
        component.human_name = config.get('human_name')
    else:
        component = models.Component(
            name=component_name,
            human_name=config.get('human_name'),
        )
    component.save()
    return component


def get_component_config(name):
    component = models.Component.objects.get(name=name)
    return component.data


def get_device_config(name):
    device = models.Device.objects.get(name=name)
    return device.data


def update_devices(name):
    comp = models.Component.objects.get(name=name)
    return comp.data
