import asyncio
import importlib
import time

from core import const
from myhome.models import Device
from myhome import mqtt


async def aio_initiate(engine, component_list):
    known_devices = Device.objects.all()
    tracker = Tracker(engine, known_devices)

    async def setup_explorer(component):
        module = importlib.import_module(f'components.{component.uniq_id}')
        explorer = await engine.loop_create_task(module.get_explorer, component.data)
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
            device = device.refresh(**data)
        else:
            device = Device(**data)
            mqtt.publish_event('event/devicexplorer/new_device', 'new_device')

        now = time.time()
        if not device.last_saved or device.last_saved < now - 5 * 60:
            device.last_saved = now
            device.save()

        self.devices[device.uniq_id] = device

    def do_exploring(self, explorer, component):
        interval = component.data.get('interval', 10)

        @self.engine.eventbus.listen(const.EVENT_TIME_CHANGED)
        def _explore_devices():
            loop_time = self.engine.loop.time()
            r = round(loop_time) % interval
            if not r:
                # print(f'{loop_time} -- {r} -- {interval} -- {component.name}')
                devices = explorer.exploring_devices()
                for d in devices:
                    d['component'] = component
                    self.handle(d)


class BaseExplorer:
    def exploring_devices(self):
        raise NotImplementedError()
