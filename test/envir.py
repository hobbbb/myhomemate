import asyncio


async def aio_scanning():
    while True:
        print("1 scanning")
        await asyncio.sleep(1)
        return 1


async def aio_once():
    print("3 once")
    await asyncio.sleep(3)


async def coro2():
    loop = asyncio.get_event_loop()
    init_time = loop.time()
    while True:
        print("timer")
        print(loop.time() - init_time)
        await asyncio.sleep(3)


async def coro3():
    print("3 Worker Executed")
    stopped = asyncio.Event()
    await stopped.wait()
