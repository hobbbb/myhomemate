import sys
import asyncio
import uvloop

import core


async def init_myhomemate():
    mhm = core.MyHomeMate()
    return await mhm.async_run()


if __name__ == "__main__":
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    asyncio.run(init_myhomemate())
    #sys.exit(main())
