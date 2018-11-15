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

from myhome import models


class EventBus:
    # __slots__ = '_events'

    def __init__(self):
        self._events = defaultdict(set)

    def listen(self, event):
        def outer(func):
            self._add_event(event, func)

            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper

        return outer

    def throw(self, event):
        for func in self._event_funcs(event):
            # func(*args, **kwargs)
            func()

    def _event_funcs(self, event):
        for func in self._events[event]:
            yield func

    def _add_event(self, event, func):
        self._events[event].add(func)


class HomeEngine:
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.eventbus = EventBus()

    async def aio_run(self):
        self.eventbus.throw('start_engine')

        print('run')
        await asyncio.sleep(1)

    # def aio_add_job(self, tgt, *args):
    #     if asyncio.iscoroutine(tgt):
    #         print('1')
    #     elif asyncio.iscoroutinefunction(tgt):
    #         print('2')
    #     else:
    #         print('3')

    #     # self.loop.call_soon(tgt, *args)
    #     # task = self.loop.run_in_executor(None, tgt, *args)

    #     # task = self.loop.create_task(tgt)
    #     # return task
    #     return


async def aio_configuration(engine):
    qs = models.Component.objects.filter(is_active=True)
    for c in qs:
        try:
            module = importlib.import_module('components.{}'.format(c.name))
        except ModuleNotFoundError:
            raise()

        if hasattr(module, 'get_scanner'):
            scanner = module.get_scanner(c.data)
        elif hasattr(module, 'init_component'):
            module.init_component(engine, c.data)

        print(engine.eventbus.__dict__)
        # await engine.aio_add_job(scanner.scan_devices)
        # engine.loop.create_task(scanner.aio_scan_devices())

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
