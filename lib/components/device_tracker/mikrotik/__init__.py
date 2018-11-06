# -*- encoding: utf-8 -*-

from django import forms

from myhome.api import register_component


def register():
    register_component({
        'human_name': 'Mikrotik',
    })


class SetupForm(forms.Form):
    host = forms.CharField(max_length=50, initial='192.168.88.1')
    port = forms.IntegerField(initial=8728)
    user = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)
