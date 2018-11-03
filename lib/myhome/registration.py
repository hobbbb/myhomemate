import inspect
import re

from myhome import models


def register(config):
    component_name = re.sub(r'(^lib/components/)|(/registration.py$)', '', inspect.stack()[1][1]).replace('/', '.')
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
