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

    return 1


class Device:
    def __init__(self, *args, **kwargs):
        print(kwargs)

class BaseExplorer:
    def exploring_devices(self):
        raise NotImplementedError()
