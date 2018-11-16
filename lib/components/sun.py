# -*- encoding: utf-8 -*-

import logging

from django import forms

from myhome.api import register_component


REQUIREMENTS = ['astral==1.7.1']


logger = logging.getLogger(__name__)


def register():
    register_component({
        'human_name': 'Солнце',
    })


class ComponentSetupForm(forms.Form):
    token = forms.CharField(label='Токен', max_length=100)
    proxy_url = forms.CharField(max_length=100, required=False)
    proxy_user = forms.CharField(max_length=100, required=False)
    proxy_password = forms.CharField(max_length=100, required=False, widget=forms.PasswordInput)


def init_component(engine, config):
    import astral

    return True
