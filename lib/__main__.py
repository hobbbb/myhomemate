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

    async def async_run(self):
        print('run')
        await asyncio.sleep(1)


async def aio_configuration(engine):
    qs = models.Component.objects.filter(is_active=True)
    for c in qs:
        try:
            module = importlib.import_module('components.{}'.format(c.name))
        except ModuleNotFoundError:
            raise()

        # loop.create_task(module.aio_run())
    print('aio_configuration')
    await asyncio.sleep(3)


async def setup_and_run():
    engine = HomeEngine()

    await aio_configuration(engine)

    await engine.async_run()


if __name__ == "__main__":
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    asyncio.run(setup_and_run())
