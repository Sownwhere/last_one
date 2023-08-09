from imports import *
from Glob import Glob
import Prerequisites as preq
from decisions import *
from sleep_state import *
from awake_state import *
from receive import *
import datetime
from datetime import datetime
import pandas as pd

global data
data=[]

async def recvpump(ws):
    """Empty the recv buffer, doing nothing with the messages."""
    while True:
        await ws.recv()
        
async def squid_game(ws):       
    
    global data

    while True:
        
        await asyncio.sleep(0.2)
        prostate = Glob.finalstate
        if prostate == 0:
            print("pass")
            await asyncio.sleep(0.1)

        elif prostate == 1:                         # STATE 1
            
            if len(data)>0:
                #DATA SAVING
                current_datetime = datetime.now().strftime("%Y-%m-%d %H_%M_%S")  
                usb_key_path = r"C:\Users\Science Gallery\Desktop\Data"  # Replace with the path you want it to save to
                file_name = f"data_{current_datetime}.xlsx"
                file_path = usb_key_path + "\\" + file_name  # Use double backslashes to escape the backslash character
                try:
                    df = pd.DataFrame(data)  # Create a DataFrame from the data
                    df.to_excel(file_path, index = False)  # Save the DataFrame to Excel without header
                    data = []  # Reset the data list
                except Exception as e:
                    print("Error occurred while saving the Excel file:", str(e))
            else:
                pass

            await SLEEPING(ws)


        elif prostate >= 2:

            try:
                # Save their data and keep appending it while they're there
                data.append([datetime.now().strftime("%Y-%m-%d %H_%M_%S"), Glob.current_behaviour, Glob.Position, Glob.Velocity, Glob.distance, Glob.threedim, Glob.twodim,  Glob.p, Glob.l0, Glob.l1])
            except Exception as e:
                print("Error occurred while saving the Excel file:", str(e))            
            
            await AWAKE(ws)


async def main_functions(actions,zed_signal_attrs, lock1,lock2):    

    async with websockets.connect(f"ws://10.20.24.10:5555/ws", ping_interval=5, ping_timeout=5) as ws:
        while True:
            tasks = [ 
            asyncio.ensure_future(receive_data(actions,zed_signal_attrs, lock1,lock2)),                                      # running concurrently:    
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


