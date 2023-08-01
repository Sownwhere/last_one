from imports import *
from Glob import Glob
import Prerequisites as preq
from decisions import *
from sleep_state import *
from awake_state import *
from recive import *

async def recvpump(ws):
    """Empty the recv buffer, doing nothing with the messages."""
    while True:
        await ws.recv()
        
async def squid_game(ws):       
    
    while True:
        
        await asyncio.sleep(0.2)
        prostate = Glob.finalstate
        if prostate == 0:
            print("pass")
            await asyncio.sleep(0.1)

        elif prostate == 1:                         # STATE 1

            print("sleeping none seen")

            await SLEEPING(ws)

            print('end of sleeping non seen')

        elif prostate >= 2:

            print('awake')
            
            await AWAKE(ws)

            print('end awake')

async def main_functions(actions,zed_signal_attrs, lock1,lock2):    

    async with websockets.connect(f"ws://10.20.24.10:5555/ws", ping_interval=5, ping_timeout=5) as ws:
        while True:
            tasks = [ 
            asyncio.ensure_future(recive_data(actions,zed_signal_attrs, lock1,lock2)),                                      # running concurrently:    
            asyncio.ensure_future(decision()),               # decides which state per 10 readings
            asyncio.ensure_future(squid_game(ws)),           # decides which behaviours
            asyncio.ensure_future(recvpump(ws))              # clears buffer
            ]
            
            await asyncio.wait(tasks)     

if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s %(message)s",
        level=logging.CRITICAL #.DEBUG,
    )
    
    asyncio.run(main_functions())                                # vary tested function here


