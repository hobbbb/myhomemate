# -*- encoding: utf-8 -*-

import librouteros
import logging

from django import forms
from myhome.api import register_component, get_component_config, update_devices


_LOGGER = logging.getLogger(__name__)


def register():
    register_component({
        'human_name': 'Mikrotik',
    })


class SetupForm(forms.Form):
    host = forms.CharField(max_length=50, initial='192.168.88.1')
    port = forms.IntegerField(initial=8728)
    user = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)


class MikrotikScanner():
    def __init__(self, config):
        self.last_results = {}

        self.host = config['host']
        self.port = config['port']
        self.username = config['username']
        self.password = config['password']

        self.connected = False
        self.success_init = False
        self.client = None
        self.wireless_exist = None
        self.success_init = self.connect_to_device()

        if self.success_init:
            _LOGGER.info(
                "Start polling Mikrotik (%s) router...",
                self.host
            )
            self._update_info()
        else:
            _LOGGER.error(
                "Connection to Mikrotik (%s) failed",
                self.host
            )

    def connect_to_device(self):
        try:
            self.client = librouteros.connect(
                self.host,
                self.username,
                self.password,
                port=int(self.port),
                encoding='utf-8'
            )

            try:
                routerboard_info = self.client(cmd='/system/routerboard/getall')
            except (librouteros.exceptions.TrapError,
                    librouteros.exceptions.MultiTrapError,
                    librouteros.exceptions.ConnectionError):
                routerboard_info = None
                raise

            if routerboard_info:
                _LOGGER.info("Connected to Mikrotik %s with IP %s",
                             routerboard_info[0].get('model', 'Router'),
                             self.host)

                self.connected = True

                try:
                    self.capsman_exist = self.client(
                        cmd='/caps-man/interface/getall'
                    )
                except (librouteros.exceptions.TrapError,
                        librouteros.exceptions.MultiTrapError,
                        librouteros.exceptions.ConnectionError):
                    self.capsman_exist = False

                if not self.capsman_exist:
                    _LOGGER.info(
                        'Mikrotik %s: Not a CAPSman controller. Trying '
                        'local interfaces ',
                        self.host
                    )

                try:
                    self.wireless_exist = self.client(
                        cmd='/interface/wireless/getall'
                    )
                except (librouteros.exceptions.TrapError,
                        librouteros.exceptions.MultiTrapError,
                        librouteros.exceptions.ConnectionError):
                    self.wireless_exist = False

                if not self.wireless_exist:
                    _LOGGER.info(
                        'Mikrotik %s: Wireless adapters not found. Try to '
                        'use DHCP lease table as presence tracker source. '
                        'Please decrease lease time as much as possible.',
                        self.host
                    )

        except (librouteros.exceptions.TrapError,
                librouteros.exceptions.MultiTrapError,
                librouteros.exceptions.ConnectionError) as api_error:
            _LOGGER.error("Connection error: %s", api_error)

        return self.connected

    def scan_devices(self):
        self._update_info()
        return [device for device in self.last_results]

    def get_device_name(self, device):
        return self.last_results.get(device)

    def _update_info(self):
        if self.capsman_exist:
            devices_tracker = 'capsman'
        elif self.wireless_exist:
            devices_tracker = 'wireless'
        else:
            devices_tracker = 'ip'

        _LOGGER.info(
            "Loading %s devices from Mikrotik (%s) ...",
            devices_tracker,
            self.host
        )

        device_names = self.client(cmd='/ip/dhcp-server/lease/getall')
        if devices_tracker == 'capsman':
            devices = self.client(
                cmd='/caps-man/registration-table/getall'
            )
        elif devices_tracker == 'wireless':
            devices = self.client(
                cmd='/interface/wireless/registration-table/getall'
            )
        else:
            devices = device_names

        if device_names is None and devices is None:
            return False

        mac_names = {device.get('mac-address'): device.get('host-name')
                     for device in device_names
                     if device.get('mac-address')}

        if self.wireless_exist or self.capsman_exist:
            self.last_results = {
                device.get('mac-address'):
                    mac_names.get(device.get('mac-address'))
                for device in devices
            }
        else:
            self.last_results = {
                device.get('mac-address'):
                    mac_names.get(device.get('mac-address'))
                for device in device_names
                if device.get('active-address')
            }

        return True


def run_component():
    config = get_component_config()
    if not config:
        return

    s = MikrotikScanner(dict(
        host=config['host'],
        port=config['port'],
        username=config['user'],
        password=config['password'],
    ))

    update_devices(s.last_results)
    print(s.last_results)
