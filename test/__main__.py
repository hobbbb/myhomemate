import asyncio
import uvloop

import envir


async def main():
    await asyncio.create_task(envir.coro())
    await asyncio.create_task(envir.coro2())
    # await asyncio.create_task(envir.coro3())


if __name__ == "__main__":
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    asyncio.run(main())

# try:
#     await asyncio.create_task(simple_print())
#     await asyncio.create_task(mtik())
#     loop.run_forever()
# except KeyboardInterrupt:
#     pass
# finally:
#     print("Closing Loop")
#     loop.close()
