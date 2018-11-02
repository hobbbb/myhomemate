# import importlib
import json

from django.http import HttpResponseRedirect
from django.shortcuts import render

from myhome import models as myhome_models
from components import models as component_models

from myhome.forms import TelegramBotForm

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

    if request.method == 'POST':
        form = TelegramBotForm(request.POST)
        if form.is_valid():
            component.data_raw = json.dumps(form.cleaned_data)
            component.save()
            return HttpResponseRedirect('/components/1/')
    else:
        form = TelegramBotForm(component.data)

    data = {
        'component': component,
        'form': form,
    }
    return render(request, 'component.html', data)
