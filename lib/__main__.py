# flake8: noqa

import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myhome.settings")
django.setup()

import asyncio
import importlib
import uvloop
from collections import defaultdict
from functools import wraps

from core import const
from core.eventbus import EventBus
from myhome import models


class HomeEngine:
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.eventbus = EventBus()

    async def aio_run(self):
        print('run')

        self.eventbus.throw(const.EVENT_START_ENGINE)
        await asyncio.sleep(1)

    def aio_add_task(self, tgt, *args):
        task = self.loop.create_task(tgt)
        return task


async def aio_configuration(engine):
    print('aio_configuration')

    tasks = []

    qs = models.Component.objects.filter(is_active=True)
    for row in qs:
        sp = row.name.split('.')

        try:
            module = importlib.import_module('components.{}'.format(sp[0]))
        except ModuleNotFoundError:
            raise()

        # component_config = (sp[1], row.data) if len(sp) > 1 else row.data
        tasks.append(module.aio_initiate(engine, row))

    await asyncio.wait(tasks)
        # print(engine.eventbus.__dict__)
        # await engine.aio_add_job(scanner.scan_devices)
        # engine.loop.create_task(scanner.aio_scan_devices())

    # await asyncio.sleep(3)


async def setup_and_run():
    engine = HomeEngine()

    await aio_configuration(engine)

    return await engine.aio_run()


if __name__ == "__main__":
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    asyncio.run(setup_and_run())
