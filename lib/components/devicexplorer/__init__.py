import asyncio
import importlib
import time

from core import const
from myhome.models import Device


def schedule(func, interval, engine):
    async def periodic_func():
        while True:
            await func()
            await asyncio.sleep(interval, loop=engine.loop)

    return loop.create_task(periodic_func())


async def aio_initiate(engine, component_list):
    async def setup_explorer(component):
        module = importlib.import_module(f'components.{component.uniq_id}')
        cfg = component.data
        interval = cfg.get('interval', 10)

        # if hasattr(module, 'aio_get_explorer'):
        #     explorer = await asyncio.wait([module.aio_get_explorer(cfg)])
        if hasattr(module, 'get_explorer'):
            explorer = module.get_explorer(cfg)

    # tasks = [setup_explorer(c) for c in component_list]
    # done, pending = await asyncio.wait(tasks, loop=engine.loop)

    # known_devices = component.device_set.all()
    # deviceset = DeviceSet(known_devices)

    # devices = explorer.exploring_devices()
    # for d in devices:
    #     d['component'] = component
    #     deviceset.handle(d)

    # schedule(explorer.aio_exploring_devices, interval=interval, engine=engine)

    @engine.eventbus.listen(const.EVENT_TIME_CHANGED)
    def _explore_devices():
        loop_time = engine.loop.time()
        r = round(loop_time) % 6
        print(loop_time, r)

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
