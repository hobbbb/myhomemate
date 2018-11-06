import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myhome.settings")
django.setup()

import asyncio
import importlib
import uvloop

from myhome import models


# qs = models.Component.objects.filter(is_active=True)
# for c in qs:
#     try:
#         module = importlib.import_module('components.{}'.format(c.name))
#     except ModuleNotFoundError:
#         raise()

#     module.run_component()


async def aio_main():
    qs = models.Component.objects.filter(is_active=True)
    for c in qs:
        try:
            module = importlib.import_module('components.{}'.format(c.name))
        except ModuleNotFoundError:
            raise()

        await asyncio.create_task(module.aio_run())


if __name__ == "__main__":
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    asyncio.run(aio_main())
