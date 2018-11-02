# import importlib

from django.shortcuts import render

from myhome import models as myhome_models
from components import models as component_models


def component_list(request):
    components = myhome_models.Component.objects.all()
    # for c in components:
    #     c.has_setup = 1
    #     try:
    #         importlib.import_module('components.{}.views'.format(c.name))
    #     except ModuleNotFoundError:
    #         c.has_setup = 0

    data = {
        'components': components
    }
    return render(request, 'components.html', data)


def component_setup(request, id):
    component = myhome_models.Component.objects.get(id=id)
    data = {
        'component': component
    }
    return render(request, 'component.html', data)
