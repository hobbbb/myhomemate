import asyncio
import uvloop

from mikrotik import MikrotikScanner


async def c1():
    await asyncio.sleep(1)
    print("1 Worker Executed")

async def c2():
    while True:
        print("2 Worker Executed")
        await asyncio.sleep(3)
        s = MikrotikScanner(dict(
            host = '192.168.88.1',
            username = 'admin',
            password = 'VPavelB1983',
            port = 8728,
        ))
        print(s.last_results)

async def c3():
    print("3 Worker Executed")
    stopped = asyncio.Event()
    await stopped.wait()


async def main():
    await asyncio.create_task(c1())
    await asyncio.create_task(c2())
    # await asyncio.create_task(c3())


if __name__ == "__main__":
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.get_running_loop()
    print(loop)
    asyncio.run(main())

# try:
#     await asyncio.create_task(simple_print())
#     await asyncio.create_task(mtik())
#     # asyncio.ensure_future(simple_print())
#     # asyncio.ensure_future(mtik())
#     loop.run_forever()
# except KeyboardInterrupt:
#     pass
# finally:
#     print("Closing Loop")
#     loop.close()
