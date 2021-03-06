# -*- encoding: utf-8 -*-

import asyncio
import logging
import requests
import urllib3

from django import forms

from . import BaseExplorer

NAME = 'iCloud devices'

urllib3.disable_warnings()
logger = logging.getLogger(__name__)


class ComponentSetupForm(forms.Form):
    user = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)  # , widget=forms.PasswordInput
    interval = forms.IntegerField(initial=5)


def get_explorer(config):
    return ICloudExplorer(config)


class ICloudExplorer(BaseExplorer):
    def __init__(self, config):
        for k, v in config.items():
            setattr(self, k, v)

        self.exploring_results = []

        # self._exploring_devices()

    def _exploring_devices(self):
        url = 'https://{}:{}@fmipmobile.icloud.com/fmipservice/device/{}/initClient'.format(
            self.user, self.password, self.user
        )
        try:
            http_resp = requests.post(url, timeout=5, verify=False)
        except requests.exceptions.RequestException as e:
            logger.error(u'exception: "{}"'.format(e))
            return

        try:
            result = http_resp.json()
        except Exception as e:
            logger.error(u'format error: "{}", result: "{}"'.format(e, http_resp.text))
            return

        self.exploring_results = []
        for d in result['content']:
            self.exploring_results.append({
                'uniq_id': d['name'],
                'name': d['name'],
                'battery': round(d.get('batteryLevel', 0) * 100) if d.get('batteryStatus', '') != 'Unknown' else None,
                'latitude': d['location']['latitude'] if d.get('location') else None,
                'longitude': d['location']['longitude'] if d.get('location') else None,
                'data': {
                    'batteryStatus': d.get('batteryStatus'),
                },
            })

    def exploring_devices(self):
        self._exploring_devices()
        return self.exploring_results
