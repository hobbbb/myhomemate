import asyncio
import uvloop

import envir


async def main():
    loop = asyncio.get_event_loop()

    tasks = [
        loop.create_task(envir.aio_scanning()),
        loop.create_task(envir.aio_once())
    ]
    loop.run_until_complete(asyncio.wait(tasks))


if __name__ == "__main__":
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    asyncio.run(main())


# if __name__ == "__main__":
#     asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
#     loop = asyncio.get_event_loop()
#     tasks = [
#         loop.create_task(envir.coro()),
#         loop.create_task(envir.coro4())
#     ]
#     loop.run_until_complete(asyncio.wait(tasks))

# try:
#     await asyncio.create_task(simple_print())
#     await asyncio.create_task(mtik())
#     loop.run_forever()
# except KeyboardInterrupt:
#     pass
# finally:
#     print("Closing Loop")
#     loop.close()
