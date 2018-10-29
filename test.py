import sys
import asyncio
import uvloop


async def init_myhome():
    print('Hello ...')
    await asyncio.sleep(1)
    print('... World!')


if __name__ == "__main__":
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    asyncio.run(init_myhome())
    #sys.exit(main())
