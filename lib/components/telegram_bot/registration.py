# -*- encoding: utf-8 -*-

from django import forms

from myhome.registration import register


class SetupForm(forms.Form):
    token = forms.CharField(label='Токен', max_length=100)
    proxy_url = forms.CharField(max_length=100, required=False)
    proxy_user = forms.CharField(max_length=100, required=False)
    proxy_password = forms.CharField(max_length=100, required=False)


def setup_component():
    config = dict(
        human_name='Телеграм',
    )
    register(config)
