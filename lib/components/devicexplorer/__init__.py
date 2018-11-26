import asyncio
import importlib
import time

from myhome.models import Device


async def aio_initiate(engine, component):
    module = importlib.import_module(f'components.{component.uniq_id}')

    cfg = component.data

    known_devices = component.device_set.all()
    deviceset = DeviceSet(known_devices)

    # if hasattr(module, 'aio_get_explorer'):
    #     explorer = await asyncio.wait([module.aio_get_explorer(cfg)])
    if hasattr(module, 'get_explorer'):
        explorer = module.get_explorer(cfg)

    interval = cfg.get('interval', 10)
    # while True:
    print(f'{component.uniq_id}...')
    # await asyncio.sleep(interval)
    await asyncio.sleep(0)

    devices = explorer.exploring_devices()
    for d in devices:
        d['component'] = component
        deviceset.handle(d)

    return 1


class DeviceSet:
    def __init__(self, devices):
        self.devices = {d.uniq_id: d for d in devices}

    def handle(self, data):
        device = self.devices.get(data['uniq_id'])
        if device:
            device = device.refresh(**data)
        else:
            device = Device(**data)

        now = time.time()
        if not device.last_saved or device.last_saved < now - 5 * 60:
            device.last_saved = now
            device.save()

        self.devices[device.uniq_id] = device


class BaseExplorer:
    def exploring_devices(self):
        raise NotImplementedError()
