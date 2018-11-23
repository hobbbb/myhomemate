import asyncio
import importlib
import time

from myhome import models


async def aio_initiate(engine, component):
    module = importlib.import_module(f'components.{component.uniq_id}')

    cfg = component.data

    known_devices = component.device_set.all()
    deviceset = EDeviceSet(known_devices)

    # if hasattr(module, 'aio_get_explorer'):
    #     explorer = await asyncio.wait([module.aio_get_explorer(cfg)])
    if hasattr(module, 'get_explorer'):
        explorer = module.get_explorer(cfg)

    interval = cfg.get('interval', 10)
    while True:
        print(f'{component.uniq_id}...')
        await asyncio.sleep(interval)

        devices = explorer.exploring_devices()
        for d in devices:
            d['component'] = component
            device = EDevice(**d)
            deviceset.handle(device)

    return 1


class EDeviceSet:
    def __init__(self, devices):
        self.devices = {d.uniq_id: d for d in devices}

    def handle(self, edevice):
        print(edevice.__dict__)
        if edevice.uniq_id in self.devices.keys():
            pass
        else:
            edevice.save()
            self.devices[edevice.uniq_id] = edevice


class EDevice:
    def __init__(self, *args, **kwargs):
        self.component = kwargs.get('component')
        self.uniq_id = kwargs.get('device_id')
        self.name = kwargs.get('name')
        self.attrs = kwargs.get('data')
        self.battery = kwargs.get('battery')
        self.longitude = kwargs.get('longitude')
        self.latitude = kwargs.get('latitude')
        self.last_saved = None

    def save(self):
        now = time.time()
        if not self.last_saved or self.last_saved < now - 5 * 60:
            self.last_saved = now
            device = models.Device.objects.filter(component=self.component, uniq_id=self.uniq_id).first()
            if device:
                device.battery = self.battery
                device.longitude = self.longitude
                device.latitude = self.latitude
                device.data = self.data
            else:
                device = models.Device(
                    is_tracking=True,
                    component=self.component,
                    uniq_id=self.uniq_id,
                    name=self.name,
                    battery=self.battery,
                    longitude=self.longitude,
                    latitude=self.latitude,
                    data=self.attrs,
                )
            device.save()


class BaseExplorer:
    def exploring_devices(self):
        raise NotImplementedError()
