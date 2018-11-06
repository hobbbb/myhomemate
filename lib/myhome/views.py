import importlib
import json

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from myhome import models as myhome_models
# from components import models as component_models


def component_list(request, filt='active'):
    cond = {}
    if filt == 'active':
        cond['is_active'] = True
    components = myhome_models.Component.objects.filter(**cond).all()
    # for c in components:
    #     c.has_setup = 1
    #     try:
    #         importlib.import_module('components.{}.views'.format(c.name))
    #     except ModuleNotFoundError:
    #         c.has_setup = 0

    data = {
        'filt': filt,
        'components': components,
    }
    return render(request, 'components.html', data)


def component_setup(request, id):
    component = myhome_models.Component.objects.get(id=id)

    try:
        module = importlib.import_module('components.{}'.format(component.name))
    except ModuleNotFoundError:
        raise()

    if request.method == 'POST':
        form = module.SetupForm(request.POST)
        if form.is_valid():
            component.data_raw = json.dumps(form.cleaned_data)
            component.save()
            return HttpResponseRedirect(reverse('act_components'))
    else:
        form = module.SetupForm(component.data)

    data = {
        'component': component,
        'form': form,
    }
    return render(request, 'component.html', data)


def device_list(request):
    devices = myhome_models.Device.objects.all()
    data = {
        'devices': devices,
    }
    return render(request, 'devices.html', data)


def device_setup(request, id):
    pass


def person_list(request):
    persons = User.objects.all()
    data = {
        'persons': persons,
    }
    return render(request, 'persons.html', data)


def person_setup(request, id):
    pass


def room_list(request):
    data = {}
    return render(request, 'rooms.html', data)


def room_setup(request, id):
    pass


def zone_list(request):
    data = {}
    return render(request, 'zones.html', data)


def zone_setup(request, id):
    pass


def log_list(request):
    data = {}
    return render(request, 'logs.html', data)
