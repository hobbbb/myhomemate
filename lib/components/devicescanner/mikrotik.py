# -*- encoding: utf-8 -*-

import logging

from django import forms

from myhome.api import register_component


REQUIREMENTS = ['librouteros==2.1.1']


logger = logging.getLogger(__name__)


def register():
    register_component({
        'human_name': 'Mikrotik',
    })


class ComponentSetupForm(forms.Form):
    host = forms.CharField(max_length=50, initial='192.168.88.1')
    port = forms.IntegerField(initial=8728)
    user = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)  # , widget=forms.PasswordInput
    interval = forms.IntegerField(initial=5)


def get_scanner(config):
    scanner = MikrotikScanner(config)
    return scanner if scanner.scan_init else None


class MikrotikScanner:
    def __init__(self, config):
        for k, v in config.items():
            setattr(self, k, v)

        self.scan_results = []
        self.scan_init = self.connect_to_device()

        if self.scan_init:
            logger.info('Start polling Mikrotik router...')
            # self._scan_devices()
        else:
            logger.error('Connection to Mikrotik failed')

    def connect_to_device(self):
        import librouteros

        try:
            self.client = librouteros.connect(
                self.host,
                self.user,
                self.password,
                port=int(self.port),
                encoding='utf-8'
            )

            try:
                routerboard = self.client(cmd='/system/routerboard/getall')
            except (librouteros.exceptions.TrapError,
                    librouteros.exceptions.MultiTrapError,
                    librouteros.exceptions.ConnectionError):
                routerboard = None
                raise

            if routerboard:
                logger.info('Connected to Mikrotik {}'.format(routerboard[0].get('model', 'Router')))

                try:
                    self.capsman_exist = self.client(cmd='/caps-man/interface/getall')
                except (librouteros.exceptions.TrapError,
                        librouteros.exceptions.MultiTrapError,
                        librouteros.exceptions.ConnectionError):
                    self.capsman_exist = False

                try:
                    self.wireless_exist = self.client(cmd='/interface/wireless/getall')
                except (librouteros.exceptions.TrapError,
                        librouteros.exceptions.MultiTrapError,
                        librouteros.exceptions.ConnectionError):
                    self.wireless_exist = False
        except (librouteros.exceptions.TrapError,
                librouteros.exceptions.MultiTrapError,
                librouteros.exceptions.ConnectionError) as api_error:
            logger.error('Connection error: {}'.format(api_error))

        return True

    def _scan_devices(self):
        if self.capsman_exist:
            devices_tracker = 'capsman'
        elif self.wireless_exist:
            devices_tracker = 'wireless'
        else:
            devices_tracker = 'ip'

        logger.info("Loading %s devices from Mikrotik (%s) ...", devices_tracker, self.host)

        device_names = self.client(cmd='/ip/dhcp-server/lease/getall')
        if devices_tracker == 'capsman':
            devices = self.client(cmd='/caps-man/registration-table/getall')
        elif devices_tracker == 'wireless':
            devices = self.client(cmd='/interface/wireless/registration-table/getall')
        else:
            devices = device_names

        if device_names is None and devices is None:
            return False

        macs = {device.get('mac-address'): device for device in device_names if device.get('mac-address')}

        self.scan_results = []
        if self.wireless_exist or self.capsman_exist:
            for device in devices:
                mac = macs.get(device.get('mac-address'))
                self.scan_results.append({
                    'name': mac['mac-address'],
                    'human_name': mac['host-name'],
                })
        else:
            for device in device_names:
                if not device.get('active-address'):
                    continue
                mac = macs.get(device.get('mac-address'))
                self.scan_results.append({
                    'name': mac['mac-address'],
                    'human_name': mac['host-name'],
                })

        return True

    def scan_devices(self):
        self._scan_devices()
        return self.scan_results

# async def aio_run():
#     await asyncio.sleep(0)

#     config = get_component_config()
#     if not config:
#         return

#     s = MikrotikScanner(dict(
#         host=config['host'],
#         port=config['port'],
#         username=config['user'],
#         password=config['password'],
#     ))

#     # update_devices(s.scan_results)
#     print(s.scan_results)
