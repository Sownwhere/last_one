
# WE BE TESTIN
# WE BE TESTIN
# WE BE TESTIN
# WE BE TESTIN
# WE BE TESTIN                  # DONT TOUCH THIS PLES
# WE BE TESTIN
# WE BE TESTIN
# WE BE TESTIN
# WE BE TESTIN

from imports import *
from Glob import Glob
import Prerequisites as preq
from skelCoord import * 
from decisions import *
from sleep_state import *
from awake_state import *

async def recvpump(ws):
    """Empty the recv buffer, doing nothing with the messages."""
    while True:
        await ws.recv()  

async def up_bloop(ws):                         # blue shift upwards continuous loop
    sta = 585
    fin = 910                                                 
    await preq.full_reset(ws)
    await asyncio.sleep(1)
    await alight_ends(ws, [255,255,255], [sta, sta, 255])
    while True:
        await flow(ws, 1, [[255,255,255],[fin,fin,255]])
        await alight_ends(ws, [255,255,255], [sta, sta, 255])

async def whee(ws):                             # values finder for testing
    sta = 585
    fin = 910                                                 
    await preq.full_reset(ws)
    for i in range(1000):
        await alight_ends(ws,[0,0,0],[20*i,0,0])
        print(i, '       ', i*20)
        await asyncio.sleep(0.3)

async def whoo(ws):                                             # the yellow green one with working normalisation
    await preq.full_reset(ws)
    await asyncio.sleep(1)
    await preq.flow(ws, 1, [[0,0,0],[255,100,0]])
    print('YABBADABBADOO')
    await asyncio.sleep(1)
    await preq.flow(ws, 2, [[0,0,0],[910,100,0]])
    await preq.flow(ws, 1, [[910,100,0],[910,100,0]])
    print('normalise')                                                          ###### normalise worked!!!!!!
    await asyncio.sleep(2)
    await preq.alight_ends(ws,[145,100,0],[145,100,0])
    print('end')

async def whew(ws):                                             # demo vid, working, dont toucc
    await preq.full_reset(ws)
    await asyncio.sleep(1)
    await simul_inflate(ws, [1,0,1])

    await preq.flow(ws, 1, [[0,0,0],[255,100,0]])    
    await simul_inflate(ws, [1,1,1])

    await asyncio.sleep(1)
    await simul_inflate(ws, [0.8,0.4,0.8])    
    await preq.flow(ws, 2, [[0,0,0],[910,100,0]])
    await preq.flow(ws, 1, [[910,100,0],[910,100,0]])
    print('normalise')                                                        
    
    await asyncio.sleep(2)
    await simul_inflate(ws, [1,1,0.2])
    await preq.alight_ends(ws,[145,100,0],[145,100,0])
    print('end')

    ###########################################################

    await preq.flow(ws, 2, [[255,255,255],[200,0,200]])
    await simul_inflate(ws, [0.2,1,0.7])
    await alight_ends(ws, [255,255,255],[965,0,965])
    await preq.flow(ws, 4, [[0,0,0],[255,255,255]])
    await simul_inflate(ws, [1,1,1])
###################################################################



async def directional_test(ws):
    await preq.full_reset(ws)
    await asyncio.sleep(3)
    await preq.alight(ws,0,700,255)

    while True:
        p = [1,1,0]
        await preq.simul_inflate(ws, p)
        await alight(ws,0,0,255)
        print(1)
        await asyncio.sleep(3)
        await preq.full_reset(ws)
        await asyncio.sleep(1)

        p = [1,0,1]
        await preq.simul_inflate(ws, p)
        print(2)
        await alight(ws,0,255,0)
        await asyncio.sleep(3)
        await preq.full_reset(ws)
        await asyncio.sleep(1)

        p = [0.2,1,1]
        await preq.simul_inflate(ws, p)
        await alight(ws,255,0,0)
        print(3)
        await asyncio.sleep(3)
        await preq.full_reset(ws)
        await asyncio.sleep(1)


async def dance(ws):

    while True:

        p0 = random.choice([0,1])
        p1 = random.choice([0,1])
        p2 = random.choice([0,1])

        r = random.uniform(0,255)
        g = random.uniform(0,255)
        b = random.uniform(0,255)

        # await preq.simul_inflate(ws, [1, 1, 1])
        # await preq.alight(ws, r, g, b)
        # await asyncio.sleep(0.5)

        await preq.simul_inflate(ws, [p1,p0,p2])
        await preq.alight(ws, r, g, b)
        await asyncio.sleep(1)




# TEST FUNCTION

async def blarp_test():    # testing

    async with websockets.connect(f"ws://10.20.24.10:5555/ws", ping_interval=5, ping_timeout=5) as ws:
        while True: 
            tasks = [
            asyncio.ensure_future(dance(ws)),                                
            #asyncio.ensure_future(preq.simul_inflate(ws,[1,1,0])),                  # test chambers
            #asyncio.ensure_future(preq.alight_ends(ws, [0,0,0],[600,600,600])),         # test lights
            asyncio.ensure_future(recvpump(ws))              
            ]
        
            await asyncio.wait(tasks) 
             

if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s %(message)s",
        level=logging.CRITICAL #.DEBUG,
    )
    
    asyncio.run(blarp_test())                                # vary tested function here