# flake8: noqa

import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myhome.settings")
django.setup()
from django.core.cache import cache
from django.utils import timezone

import asyncio
import importlib
import uvloop
from collections import defaultdict
from time import monotonic

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from core import const
from core.eventbus import EventBus, ServiceRegistry
from myhome import models


def run_timer(engine):
    def schedule_timer():
        engine.loop.call_later(1, throw_time_event)

    def throw_time_event():
        engine.eventbus.throw(const.EVENT_TIME_CHANGED)
        schedule_timer()

    schedule_timer()


async def automatization(engine):
    print('automatization')

    atmz = [
        {
            'trigger': {
                'platform': 'zone',
                'entity_id': 1,
                'event': 'enter',
            },
            'condition': {},
            'action': {
                'service': 'telegram_bot.notify',
                'data': 'test',
            },
        },
        {
            'trigger': {
                'platform': 'telegram_bot',
            },
            'condition': {},
            'action': {},
        },
    ]

    @engine.eventbus.listen(const.EVENT_ALL)
    def test(data):
        for a in atmz:
            if a['trigger']['platform'] != data.get('platform'):
                continue
            if a['trigger']['entity_id'] != data.get('entity_id'):
                continue
            if a['trigger']['event'] != data.get('event'):
                continue

            print(a)

    return True


class HomeEngine:
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.eventbus = EventBus()
        self.service = ServiceRegistry()
        self.scheduler = AsyncIOScheduler()
        self.hold = None

    async def aio_run(self):
        print('run')

        self.hold = asyncio.Event()

        self.eventbus.throw(const.EVENT_START_ENGINE, {'platform': const.PLATO_ZONE, 'event': 'enter', 'entity_id': 1})

        self.scheduler.print_jobs()
        self.scheduler.start()
        await self.hold.wait()

    def add_scheduler_job(self, target, seconds):
        self.scheduler.add_job(target, 'interval', seconds=seconds)

    def loop_create_task(self, target, *args):
        if asyncio.iscoroutine(target):
            print('iscoroutine')
            task = self.loop.create_task(target)
        elif asyncio.iscoroutinefunction(target):
            print('iscoroutinefunction')
            task = self.loop.create_task(target)
        else:
            task = self.loop.run_in_executor(None, target, *args)

        return task


async def aio_configuration(engine):
    print('aio_configuration')

    # @engine.eventbus.listen(const.EVENT_START_ENGINE)
    # def _run_timer():
    #     run_timer(engine)

    zones = {z.id: z for z in models.Zone.objects.all()}
    cache.set('zones', zones, None)

    components = defaultdict(list)
    qs = models.Component.objects.filter(is_active=True)
    for row in qs:
        sp = row.uniq_id.split('.')
        if len(sp) > 1:
            components[sp[0]].append(row)
        else:
            components[sp[0]] = row

    tasks = []
    for name, data in components.items():
        module = importlib.import_module(f'components.{name}')
        tasks.append(module.aio_initiate(engine, data))

    tasks.append(automatization(engine))

    qs = models.Script.objects.all()
    for row in qs:
        def _script():
            exec(row.text)
        # engine.add_scheduler_job(_script, 1)

    await asyncio.wait(tasks)


async def setup_and_run():
    engine = HomeEngine()

    await aio_configuration(engine)

    return await engine.aio_run()


if __name__ == "__main__":
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.new_event_loop()
    loop.set_debug(True)
    try:
        asyncio.run(setup_and_run())
    except KeyboardInterrupt:
        loop.stop()
