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
    return component.data


def update_devices(devices):
    component_name = utils.component_name()
    component = models.Component.objects.get(name=component_name)
    print(component.devices_set)
