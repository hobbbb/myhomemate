import importlib

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from myhome import forms, models


def main(request):
    devices = models.Device.objects.all()
    data = {
        'devices': devices,
    }
    return render(request, 'main.html', data)


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


def component_edit(request, id):
    component = models.Component.objects.get(id=id)
    component_module = importlib.import_module(f'components.{component.uniq_id}')

    if request.method == 'POST':
        form = component_module.ComponentSetupForm(request.POST)
        if form.is_valid():
            component.data = form.cleaned_data
            component.save()
            return HttpResponseRedirect(reverse('act_components'))
    else:
        form = component_module.ComponentSetupForm(component.data)

    data = {
        'component': component,
        'form': form,
    }
    return render(request, 'component_edit.html', data)


def device_list(request, component_id=None):
    component = models.Component.objects.get(id=1)
    component_module = importlib.import_module(f'components.{component.uniq_id}')
    editable = True if hasattr(component_module, 'DeviceSetupForm') else False

    data = {
        'devices': component.device_set.all(),
        'editable': editable,
    }
    return render(request, 'devices.html', data)


def device_edit(request, id):
    device = models.Device.objects.get(id=id)
    component_module = importlib.import_module(f'components.{device.component.name}')

    if request.method == 'POST':
        form = component_module.DeviceSetupForm(request.POST)
        # if form.is_valid():
        #     component.data = json.dumps(form.cleaned_data)
        #     component.save()
        #     return HttpResponseRedirect(reverse('act_components'))
    else:
        form = component_module.DeviceSetupForm(device.data)

    data = {
        'device': device,
        'form': form,
    }
    return render(request, 'device_edit.html', data)


def person_list(request):
    persons = User.objects.all()
    data = {
        'persons': persons,
    }
    return render(request, 'persons.html', data)


def person_edit(request, id):
    pass


def room_list(request):
    data = {}
    return render(request, 'rooms.html', data)


def room_edit(request, id):
    pass


def zone_list(request):
    zones = models.Zone.objects.all()
    data = {
        'zones': zones,
    }
    return render(request, 'zones.html', data)


def zone_edit(request, id=None):
    if id:
        zone = models.Zone.objects.get(pk=id)
        if request.method == 'POST':
            form = forms.ZoneForm(request.POST, instance=zone)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('zone_list'))
        else:
            form = forms.ZoneForm(instance=zone)
    else:
        if request.method == 'POST':
            form = forms.ZoneForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('zone_list'))
        else:
            form = forms.ZoneForm()

    data = {
        'form': form
    }
    return render(request, 'zone_edit.html', data)


def automation_list(request):
    automations = models.Automation.objects.all()

    data = {
        'automations': automations,
    }
    return render(request, 'automations.html', data)


def automation_edit(request, id):
    pass


def log_list(request):
    data = {}
    return render(request, 'logs.html', data)
