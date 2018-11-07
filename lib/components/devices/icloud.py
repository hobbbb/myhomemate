# -*- encoding: utf-8 -*-

import asyncio
import librouteros
import logging

import requests

from django import forms
from myhome.api import register_component, get_component_config, update_devices


_LOGGER = logging.getLogger(__name__)


def register():
    register_component({
        'human_name': 'iCloud devices',
    })


class ComponentSetupForm(forms.Form):
    user = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)


async def aio_run():
    await asyncio.sleep(0)

    config = get_component_config()
    if not config:
        return

    url = 'https://{}:{}@fmipmobile.icloud.com/fmipservice/device/{}/initClient'.format(config['user'], config['password'], config['user'])
    try:
        http_resp = requests.post(url, timeout=2, allow_redirects=False, verify=False)
    except requests.exceptions.RequestException as e:
        _LOGGER.error(u'exception: "{}"'.format(e))
        return

    try:
        result = http_resp.json()
    except Exception as e:
        _LOGGER.error(u'format error: "{}", result: "{}"'.format(e, http_resp.text))
        return

    last_results = []
    for d in result['content']:
        # print(d.keys())
        # print(d['batteryLevel'])
        last_results.append({
            'name': d['name'],
            'human_name': d['name'],
            'data': {
                # 'latitude': d['location']['latitude'],
                # 'longitude': d['location']['longitude'],
                'battery': d['batteryLevel']
                # 'batteryStatus': d['batteryStatus'],
            },
        })

    # update_devices(last_results)
    print(last_results)
