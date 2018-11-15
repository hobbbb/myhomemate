# -*- encoding: utf-8 -*-

import asyncio
import logging

import requests
import urllib3

from django import forms
from myhome.api import register_component  # , get_component_config, update_devices


logger = logging.getLogger(__name__)
urllib3.disable_warnings()


def register():
    register_component({
        'human_name': 'iCloud devices',
    })


class ComponentSetupForm(forms.Form):
    user = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)  # , widget=forms.PasswordInput
    interval = forms.IntegerField(initial=5)


def get_scanner(config):
    return ICloudScanner(config)


class ICloudScanner:
    def __init__(self, config):
        for k, v in config.items():
            setattr(self, k, v)

        self.scan_results = []

        # self._scan_devices()

    def _scan_devices(self):
        url = 'https://{}:{}@fmipmobile.icloud.com/fmipservice/device/{}/initClient'.format(
            self.user, self.password, self.user
        )
        try:
            http_resp = requests.post(url, timeout=2, verify=False)
        except requests.exceptions.RequestException as e:
            logger.error(u'exception: "{}"'.format(e))
            return

        try:
            result = http_resp.json()
        except Exception as e:
            logger.error(u'format error: "{}", result: "{}"'.format(e, http_resp.text))
            return

        self.scan_results = []
        for d in result['content']:
            self.scan_results.append({
                'name': d['name'],
                'human_name': d['name'],
                'latitude': d['location']['latitude'] if d.get('location') else None,
                'longitude': d['location']['longitude'] if d.get('location') else None,
                'data': {
                    'battery': round(d['batteryLevel'] * 100),
                    'batteryStatus': d['batteryStatus'],
                },
            })

    def scan_devices(self):
        self._scan_devices()
        return self.scan_results

    async def aio_scan_devices(self):
        await asyncio.sleep(self.interval)
        self._scan_devices()
        return self.scan_results
