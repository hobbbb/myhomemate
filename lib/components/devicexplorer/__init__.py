import asyncio
import importlib

from myhome.api import update_device


async def aio_initiate(engine, component):
    try:
        module = importlib.import_module(f'components.{component.uniq_id}')
    except ModuleNotFoundError:
        raise()

    cfg = component.data

    known_devices = component.device_set.all()
    deviceset = EDeviceSet(known_devices)

    # if hasattr(module, 'aio_get_explorer'):
    #     explorer = await asyncio.wait([module.aio_get_explorer(cfg)])
    if hasattr(module, 'get_explorer'):
        explorer = module.get_explorer(cfg)

    interval = cfg.get('interval', 10)
    while True:
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
            print('stored')
        else:
            print('new')
            edevice.save()
            self.devices[edevice.uniq_id] = edevice


class EDevice:
    def __init__(self, *args, **kwargs):
        self.component = kwargs.get('component')
        self.uniq_id = kwargs.get('device_id')
        self.name = kwargs.get('name')
        self.attrs = kwargs.get('data')
        self.battery = kwargs.get('battery')

    def save(self):
        update_device(self)


class BaseExplorer:
    def exploring_devices(self):
        raise NotImplementedError()
