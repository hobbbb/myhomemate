
import json
import logging

from myhome import models, utils


def register_component(config):
    component_id = utils.component_name()
    component = models.Component.objects.filter(uniq_id=component_id).first()
    if component:
        component.human_name = config.get('name')
    else:
        component = models.Component(
            uniq_id=component_id,
            name=config.get('name'),
            data={}
        )
    component.save()
    return component


def get_component_config():
    component_id = utils.component_name()
    component = models.Component.objects.get(uniq_id=component_id)
    if not component.data:
        logging.error('{}: component configuration is not set'.format(component.name))
        return
    return component.data


def update_devices(devices):
    component_name = utils.component_name()
    component = models.Component.objects.get(name=component_name)
    devs = {d.name: d for d in component.device_set.all()}
    for d in devices:
        if not d.get('name'):
            continue

        device = devs.get(d['name'])
        if not device:
            device = models.Device(
                component=component,
                name=d['name'],
                human_name=d.get('human_name'),
            )

        device.data = json.dumps(d.get('data'))
        device.latitude = d.get('latitude')
        device.longitude = d.get('longitude')
        device.save()


def update_device(edev):
    device = models.Device.objects.filter(component=edev.component, uniq_id=edev.uniq_id).first()
    if device:
        print('device in db')
    else:
        print('no device in db')


def get_device_config(name):
    device = models.Device.objects.get(name=name)
    return device.data
