### 森罗万象 i hate myself. lets go

from imports import *
from Glob import Glob
from Prerequisites import *
from skelCoord import *
from decisions import *

async def awaken(ws):             # rouse from sleep. Uninterruptible until complete

    Glob.current_behaviour = 'awakening...'

    wake_type = random.choice([1,2,3,4,5])
    print(wake_type)

    async def greet():
        await asyncio.sleep()
        await preq.alight_ends(ws, [])

    async def bloom():
        print('bloom')

    async def wink(ws):                 # 2 ~# bruh     # colour change one atm
        print('wink')
        downtime = 1.5 
        down = [[0,0,0], [0,0,0]]
        await preq.flow(ws, downtime, down)
        uptime = 1.5
        up = [[30,255,30], [30,255,730]]
        await preq.flow(ws, uptime, up)
        await preq.simul_inflate(ws, [1,1,1])

    if wake_type == 1:
        pass

    elif wake_type == 2:            #########################################
        pass

    elif wake_type == 3:
        pass

    Glob.current_state = 'AWAKE'
                        
async def waiting(ws):
    
    if Glob.current_behaviour != 'waiting':

        Glob.current_behaviour = 'waiting'
        Glob.start_time = time.time()
        Glob.t = 0

        Glob.patience = random.uniform(3,5)     # how long until seeking a reaction

        print('initialise wait')

    elif Glob.current_behaviour == 'waiting':

        Glob.current_behaviour = 'waiting'
        Glob.t = time.time() - Glob.start_time

    if Glob.t < Glob.patience:
        f = 0 # do the waiting behaviour here

    elif Glob.t >= Glob.patience:       # greet 

        
        


async def AWAKE(ws):              ### ### STATE FUNCTION - OVERARCHING STRUCTURE ### ###

    global current_state, current_behaviour
    global start_time, t, duration
    global p, l0, l1

    data = []

    if Glob.current_state != 'AWAKE':
        print('awaken')
        await awaken(ws)
        print('done')
        Glob.current_state == 'AWAKE'

    elif Glob.current_state == 'AWAKE':    
        
    ### DATA SAVING #######################################################################################################################################

        def save_data_to_excel(data, file_path):
            #print('a')
            df = pd.DataFrame(data)  # Create a DataFrame from the data
            #print('b')
            #print(data)
            #print('df is', df)
            df.to_excel(file_path, index = False)  # Save the DataFrame to Excel without header
            #print('c')
            data = []  # Reset the data list
            #print('d')

        # Your data collection logic goes here
        # Append the collected data to the 'data' list

        interval_minutes = 1  # Time interval in minutes

        current_minutes = time.localtime().tm_min
        current_seconds = time.localtime().tm_sec
        print(current_minutes,current_seconds)

        if current_minutes%interval_minutes==0 and current_seconds==0:
            #print('1')
            current_datetime = datetime.now().strftime("%Y-%m-%d %H_%M_%S")  # Replace colon with underscore
            #print('2')
            #data.append(0)
            data.append([current_datetime, Glob.current_behaviour, Glob.threedim, Glob.twodim, Glob.Position, Glob.Velocity, Glob.p, Glob.l0, Glob.l1])
            #print('3')
            usb_key_path = r"C:\Users\Science Gallery\Desktop\Data"  # Replace with the actual path to your USB key
            file_name = f"data_{current_datetime}.xlsx"
            file_path = usb_key_path + "\\" + file_name  # Use double backslashes to escape the backslash character
            try:
                save_data_to_excel(data, file_path)
            except Exception as e:
                print("Error occurred while saving the Excel file:", str(e))
          
    ########################################################################################################################################

        print('waving is', signal_Waving())
        print('bowing is', math_bowing())
        print('hugging is',signal_hug(Glob.distance))
        
        if signal_Waving() and (Glob.distance < 2 and (signal_hug(Glob.distance)!=True and math_bowing()!=True and signal_tickle(Glob.distance_lhand,Glob.distance_rhand)!=True)):
            f = 0   ############################################
            # print('waving')
            # await preq.waving(ws)
            
        elif math_bowing():
            f = 0   ############################################
            # print('bows')
            # await preq.bow(ws, Glob.sextant)
            
        elif signal_hug(Glob.distance) and Glob.distance<2:
            f = 0   ############################################
            # print('hug')
            # await hug(ws)
        
        elif signal_hug(Glob.distance)!=True and signal_tickle(Glob.distance_lhand,Glob.distance_rhand)==True:
            f = 0   ############################################
            # Glob.current_behaviour = 'tickling'
            # print('tickle')
            # await tickle(ws)
            
        elif (signal_Waving() and math_bowing() and signal_hug(Glob.distance))!= True:     
            f = 0   ############################################
            print('waiting')
            await waiting(ws)

#############################################   TEST  ##########################################################


async def seek(ws, sextant):
    
    if sextant == 6 or sextant == 1:
        await simul_inflate(ws, [1,0,1])

    elif sextant == 2 or sextant == 3:
        await simul_inflate(ws, [0,1,1])

    elif sextant == 4 or sextant == 5:
        await simul_inflate(ws, [1,1,0])
    
    else:
        pass



async def recvpump(ws):
    """Empty the recv buffer, doing nothing with the messages."""
    while True:
        await ws.recv()

async def yaught(ws):
    while True:
        await seek(ws,1)
        await asyncio.sleep(1)
        await seek(ws,2)
        await asyncio.sleep(1)
        await seek(ws,3)
        await asyncio.sleep(1)
        await seek(ws,4)
        await asyncio.sleep(1)
        await seek(ws,5)
        await asyncio.sleep(1)
        await seek(ws,6)
        await asyncio.sleep(1)

async def test():    # testing continuously

    async with websockets.connect(f"ws://10.20.24.10:5555/ws", ping_interval=5, ping_timeout=5) as ws:
            while True:
                tasks = [                                       
                asyncio.ensure_future(yaught(ws)),                
                asyncio.ensure_future(recvpump(ws))             
                ]
                await asyncio.wait(tasks)    


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s %(message)s",
        level=logging.CRITICAL #.DEBUG,
    )

    asyncio.run(test())     