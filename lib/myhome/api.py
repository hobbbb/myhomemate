
import json
import logging

from myhome import models, utils


def register_component(module):
    component_id = utils.component_name(module)
    component = models.Component.objects.filter(uniq_id=component_id).first()
    name = getattr(module, 'NAME')
    if component:
        component.human_name = name
    else:
        component = models.Component(
            uniq_id=component_id,
            name=name,
        )
    component.save()
    return component
