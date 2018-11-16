import asyncio
import importlib

async def aio_initiate(engine, data):
    await asyncio.sleep(2)
    print('deviceexplorer')
    return

    explorer, cfg = data

    try:
        module = importlib.import_module(f'components.deviceexplorer.{explorer}')
    except ModuleNotFoundError:
        raise()

    if hasattr(module, 'aio_get_explorer'):
        explorer = await asyncio.wait([module.aio_get_explorer(cfg)])

    return 1


class Explorer:
    def exploring_devices(self):
        raise NotImplementedError()
