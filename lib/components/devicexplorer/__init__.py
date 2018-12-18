import asyncio
import importlib
import time

from django.core.cache import cache

from core import const
from myhome.models import Device


async def aio_initiate(engine, component_list):
    known_devices = Device.objects.all()
    tracker = Tracker(engine, known_devices)

    async def setup_explorer(component):
        module = importlib.import_module(f'components.{component.uniq_id}')
        print(component.uniq_id)
        explorer = await engine.loop_create_task(module.get_explorer, component.data)
        if explorer:
            tracker.do_exploring(explorer, component)

    tasks = [setup_explorer(c) for c in component_list]
    await asyncio.wait(tasks, loop=engine.loop)


class Tracker:
    def __init__(self, engine, devices):
        self.engine = engine
        self.devices = {d.uniq_id: d for d in devices}

    def handle(self, data):
        device = self.devices.get(data['uniq_id'])
        if device:
            for k in ['latitude', 'longitude', 'battery']:
                setattr(device, k, data.get(k))

            if device.is_tracker is True:
                zones = cache.get('zones')
                for _, zn in zones.items():
                    in_zone = zn.verification(device.latitude, device.longitude)
                    if device.zone != zn.id:
                        self.engine.eventbus.throw(const.EVENT_ZONE_CHANGED, const.PLATO_ZONE)
                        print('zone changed !!!!')
                    if in_zone is True:
                        device.zone = zn.id
                    else:
                        device.zone = None
        else:
            device = Device(**data)
            self.engine.eventbus.throw(const.EVENT_NEW_DEVICE_FOUND)
        device.save()

        self.devices[device.uniq_id] = device

    def do_exploring(self, explorer, component):
        interval = component.data.get('interval', 10)

        def _explore_devices():
            loop_time = self.engine.loop.time()
            print(f'{loop_time} -- {interval} -- {component.name}')
            devices = explorer.exploring_devices()
            for d in devices:
                d['component'] = component
                self.handle(d)

        self.engine.add_scheduler_job(_explore_devices, interval)


class BaseExplorer:
    def exploring_devices(self):
        raise NotImplementedError()
