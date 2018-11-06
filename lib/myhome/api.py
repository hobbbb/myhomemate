import logging

from myhome import models, utils


def register_component(config):
    component_name = utils.component_name()
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


def get_component_config():
    component_name = utils.component_name()
    component = models.Component.objects.get(name=component_name)
    if not component.data:
        logging.error('{}: component configuration is not set'.format(component.name))
        return
    return component.data


def update_devices(new_devices):
    component_name = utils.component_name()
    component = models.Component.objects.get(name=component_name)
    device = {d.name: d for d in component.device_set.all()}
    for k, v in new_devices.items():
        if not device.get(k):
            d = models.Device(
                name=k,
                human_name=v,
                component=component
            )
            d.save()


def get_device_config(name):
    device = models.Device.objects.get(name=name)
    return device.data
