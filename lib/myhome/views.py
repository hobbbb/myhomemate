import importlib
import json

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from myhome import models


def component_list(request, filt='active'):
    cond = {}
    if filt == 'active':
        cond['is_active'] = True
    components = models.Component.objects.filter(**cond).all()
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
    component = models.Component.objects.get(id=id)

    try:
        module = importlib.import_module('components.{}'.format(component.name))
    except ModuleNotFoundError:
        raise()

    if request.method == 'POST':
        form = module.ComponentSetupForm(request.POST)
        if form.is_valid():
            component.data_raw = json.dumps(form.cleaned_data)
            component.save()
            return HttpResponseRedirect(reverse('act_components'))
    else:
        form = module.ComponentSetupForm(component.data)

    data = {
        'component': component,
        'form': form,
    }
    return render(request, 'component.html', data)


def device_list(request, component_id=None):
    component = models.Component.objects.get(id=1)

    try:
        module = importlib.import_module('components.{}'.format(component.name))
    except ModuleNotFoundError:
        raise()

    editable = True if hasattr(module, 'DeviceSetupForm') else False

    data = {
        'devices': component.device_set.all(),
        'editable': editable,
    }
    return render(request, 'devices.html', data)


def device_setup(request, id):
    device = models.Device.objects.get(id=id)

    try:
        module = importlib.import_module('components.{}'.format(device.component.name))
    except ModuleNotFoundError:
        raise()

    if request.method == 'POST':
        form = module.DeviceSetupForm(request.POST)
        # if form.is_valid():
        #     component.data_raw = json.dumps(form.cleaned_data)
        #     component.save()
        #     return HttpResponseRedirect(reverse('act_components'))
    else:
        form = module.DeviceSetupForm(device.data)

    data = {
        'device': device,
        'form': form,
    }
    return render(request, 'device.html', data)


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


def automation_list(request):
    automations = models.Automation.objects.all()

    data = {
        'automations': automations,
    }
    return render(request, 'automations.html', data)


def automation_setup(request, id):
    pass


def log_list(request):
    data = {}
    return render(request, 'logs.html', data)
