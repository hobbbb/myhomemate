import asyncio
import importlib


async def aio_initiate(engine, data):
    explorer, cfg = data

    try:
        module = importlib.import_module(f'components.devicexplorer.{explorer}')
    except ModuleNotFoundError:
        raise()

    # if hasattr(module, 'aio_get_explorer'):
    #     explorer = await asyncio.wait([module.aio_get_explorer(cfg)])
    if hasattr(module, 'get_explorer'):
        explorer = module.get_explorer(cfg)

    devices = explorer.exploring_devices()
    for d in devices:
        device = Device(**d)
        print(device.__dict__)

    return 1


class Device:
    def __init__(self, *args, **kwargs):
        self.device_id = kwargs.get('device_id')
        self.name = kwargs.get('name')
        self.attrs = kwargs.get('data')
        self.battery = kwargs.get('battery')


class BaseExplorer:
    def exploring_devices(self):
        raise NotImplementedError()
