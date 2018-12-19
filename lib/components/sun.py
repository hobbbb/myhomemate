# -*- encoding: utf-8 -*-

import logging

from django import forms


NAME = 'Солнце'
REQUIREMENTS = ['astral']

logger = logging.getLogger(__name__)


class ComponentSetupForm(forms.Form):
    token = forms.CharField(label='Токен', max_length=100)
    proxy_url = forms.CharField(max_length=100, required=False)
    proxy_user = forms.CharField(max_length=100, required=False)
    proxy_password = forms.CharField(max_length=100, required=False, widget=forms.PasswordInput)


def init_component(engine, config):
    # import astral

    return True
