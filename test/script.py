import asyncio
import functools

from concurrent.futures import ALL_COMPLETED


class FeedUpdater:
    def __init__(self, feeds, loop):
        self.feeds = feeds
        self.loop = loop

    async def _fetch(self, url):
        return url

    async def __call__(self):
        tasks = [self._fetch(url) for url in self.feeds]
        done, pending = await asyncio.wait(
            tasks,
            loop=self.loop,
            # return_when=ALL_COMPLETED
        )
        print('----')
        for task in done:
            print(task.result())


def schedule(func, args=None, kwargs=None, interval=60, *, loop):
    if args is None:
        args = []
    if kwargs is None:
        kwargs = {}

    async def periodic_func():
        while True:
            await func(*args, **kwargs)
            await asyncio.sleep(interval, loop=loop)

    return loop.create_task(periodic_func())
create_scheduler = lambda loop: functools.partial(schedule, loop=loop)


# USAGE =====================================================


loop = asyncio.new_event_loop()
scheduler = create_scheduler(loop=loop)

feeds = ['1', '2', '3']
update = FeedUpdater(feeds=feeds, loop=loop)

# scheduler(update, interval=3)
schedule(update, interval=3, loop=loop)
loop.run_forever()
