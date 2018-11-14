# flake8: noqa

import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myhome.settings")
django.setup()

import asyncio
import importlib
import uvloop

from myhome import models


class HomeEngine:
    def __init__(self):
        self.loop = asyncio.get_event_loop()

    async def aio_run(self):
        print('run')
        await asyncio.sleep(1)

    def aio_add_job(self, tgt, *args):
        if asyncio.iscoroutine(tgt):
            print('1')
        elif asyncio.iscoroutinefunction(tgt):
            print('2')
        else:
            print('3')

        # self.loop.call_soon(tgt, *args)
        task = self.loop.run_in_executor(None, tgt, *args)

        # task = self.loop.create_task(tgt)
        # return task
        return


async def aio_configuration(engine):
    qs = models.Component.objects.filter(is_active=True)
    for c in qs:
        try:
            module = importlib.import_module('components.{}'.format(c.name))
        except ModuleNotFoundError:
            raise()

        scanner = module.component_setup(c.data)
        # res = scanner.scan_devices()

        await engine.aio_add_job(scanner.scan_devices)

    print('aio_configuration')
    # await asyncio.sleep(3)


async def setup_and_run():
    engine = HomeEngine()

    await aio_configuration(engine)

    await engine.aio_run()


if __name__ == "__main__":
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    asyncio.run(setup_and_run())



"""
def aio_add_job(calb):
    loop = asyncio.get_event_loop()
    return loop.create_task(calb)


def main():
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.get_event_loop()

    component = {}
    qs = models.Component.objects.filter(is_active=True)
    for c in qs:
        try:
            module = importlib.import_module('components.{}'.format(c.name))
        except ModuleNotFoundError:
            raise()

        scanner = module.component_setup(c.data)
        res = scanner.scan_devices()

        await aio_add_job(res)

    loop.run_forever()


if __name__ == "__main__":
    main()
"""
