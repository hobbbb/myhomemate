import asyncio
import importlib


async def aio_initiate(engine, component):
    try:
        module = importlib.import_module(f'components.{component.name}')
    except ModuleNotFoundError:
        raise()

    cfg = component.data

    known_devices = component.device_set().all()
    deviceset = DeviceSet(known_devices)

    print(deviceset.devices)
    # if hasattr(module, 'aio_get_explorer'):
    #     explorer = await asyncio.wait([module.aio_get_explorer(cfg)])
    if hasattr(module, 'get_explorer'):
        explorer = module.get_explorer(cfg)

    interval = cfg.get('interval', 10)
    while True:
        await asyncio.sleep(interval)

        devices = explorer.exploring_devices()
        for d in devices:
            device = Device(**d)
            print(device.__dict__)

    return 1


class DeviceSet:
    def __init__(self, devices):
        self.devices = {d.uniq_id: d for d in devices}


class Device:
    def __init__(self, *args, **kwargs):
        self.device_id = kwargs.get('device_id')
        self.name = kwargs.get('name')
        self.attrs = kwargs.get('data')
        self.battery = kwargs.get('battery')


class BaseExplorer:
    def exploring_devices(self):
        raise NotImplementedError()
