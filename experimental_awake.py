### 森罗万象 i hate myself. lets go

from imports import *
from Glob import Glob
from Prerequisites import *
from skelCoord import *
from decisions import *

# AWAKEN - randomly choose wake up action --------------------------------------------------------------

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

# WAITING - no stimuli detected, waiting state with random motions -------------------------------------

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

        f = 0       # do the waiting behaviour here

    elif Glob.t >= Glob.patience:       # greet 

        f = 0
        
# UNDIRECTED RESPONSES - responses without direction ---------------------------------------------------

async def hug(ws):             ######################################################
    print("huggin")

    if Glob.current_behaviour != 'hugging':              # start hug

        Glob.current_behaviour = 'hugging'
        Glob.hug_type = random.choices([1,2,3], [])

        if Glob.hug_type == 1:
            g = 0
        elif Glob.hug_type == 2:
            f = 0
        elif Glob.hug_type == 3:
            f = 0
    
    elif Glob.current_behaviour == 'hugging':           # hold hug
        
        if Glob.hug_type == 1:
            g = 0
        elif Glob.hug_type == 2:
            f = 0
        elif Glob.hug_type == 3:
            f = 0

async def waving(ws):
    r = 0
    
    g_min, g_max = 190, 230
    b_min, b_max = 0, 40
    
    num_pixels = 256  # Number of pixels in the gradient
    
    for i in range(10):
        # Calculate the current position in the gradient
        position = i / (num_pixels - 1)
        
        # Use sine functions to interpolate between R and G values
        b = int(b_min + (b_max - b_min) * (math.sin(2 * math.pi * position) + 1) / 2)
        g = int(g_min + (g_max - g_min) * (math.sin(2 * math.pi * position + math.pi) + 1) / 2)
        await preq.alight_ends(ws,[r,g,b],[r,g-40,b])
    
    p = [0.3, 0.9, 0.3]
    await simul_inflate(ws, p)
    await asyncio.sleep(0.1)
    p = [0.9, 0.3, 0.3]
    await simul_inflate(ws, p)
    await asyncio.sleep(0.1)
    p = [0.3, 0.3, 0.9]
    await simul_inflate(ws, p)
    await asyncio.sleep(0.1)

async def tickle(ws):
    # r = 0
    
    # g_min, g_max = 190, 230
    # b_min, b_max = 0, 40
    
    # num_pixels = 256  # Number of pixels in the gradient
    
    # for i in range(10):
    #     # Calculate the current position in the gradient
    #     position = i / (num_pixels - 1)
        
    #     # Use sine functions to interpolate between R and G values
    #     b = int(b_min + (b_max - b_min) * (math.sin(2 * math.pi * position) + 1) / 2)
    #     g = int(g_min + (g_max - g_min) * (math.sin(2 * math.pi * position + math.pi) + 1) / 2)
    #     await preq.alight_ends(ws,[r,g,b],[r,g-40,b])
    await preq.alight_ends(ws,[0,255,0],[0,255,0])

    p = [0.5, 1, 0.5]
    await simul_inflate(ws, p)
    await asyncio.sleep(0.1)
    p = [1, 0.5, 0.5]
    await simul_inflate(ws, p)
    await asyncio.sleep(0.1)
    p = [0.5, 0.5, 1]
    await simul_inflate(ws, p)
    await asyncio.sleep(0.1)
       
async def wait(ws):     #######################################################

    print('waiting')

    if Glob.current_behaviour != 'waiting':

        Glob.current_behaviour = 'waitng'
        Glob.start_time = time.time()
        Glob.t = 0

        Glob.wait_threshold = random.uniform(5,7)       # arbitrary. adjust
        Glob.action_duration = random.uniform(5,7)      # arbitrary. adjust

    elif Glob.curent_behaviour == 'waiting':

        Glob.current_behaviour = 'waiitng'
        Glob.t = time.time() - Glob.start_time

    async def neutral(ws):
        f = 0

    async def seek(ws):
        f = 0
        
async def jumping(ws):
    print("dfffehfeuiiiefi")
    await preq.alight_ends(ws,[255,0,0],[255,0,0])
    await preq.simul_inflate(ws,[1,1,1])
    await asyncio.sleep(0.1)

# DIRECTED RESPONSES - responses based on relative position --------------------------------------------

async def bow(ws, sextant):
    
    #Glob.signBowing = True  ################# testing 
    signBowing = Glob.signBowing
    
    #await reset(ws)         ################# testing
    #await asyncio.sleep(3)  ################# testing

    if signBowing == True:
        await alight_ends(ws,[145,0,255],[145,0,255])
        #await alight_ends(ws,[0,255,0],[0,255,0])
        #print('choosing 1 to 6')

        if sextant == 0:
            print('0')
            pass
    
        elif sextant == 1:                    # radially; 0 = reach towards chamber 0
            print('1')
            await simul_inflate(ws, [1, 0, 0])
            #await asyncio.sleep(0.5)
            await asyncio.sleep(1)
            while Glob.signBowing==True :
                await simul_inflate(ws, [0.1, 0.4, 0.4])
                await asyncio.sleep(0.1)
                math_bowing()

        elif sextant == 2:
            print('2')
            await simul_inflate(ws, [1, 1, 0.2])

        elif sextant == 3:
            print('3')
            await  simul_inflate(ws, [0, 1, 0])
            await asyncio.sleep(1.2)
            while Glob.signBowing == True :
                await simul_inflate(ws, [0.6, 0.0, 0.7])
                await asyncio.sleep(0.1)
                math_bowing()

        elif sextant == 4:
            print('4')
            await simul_inflate(ws, [0.1, 0.8, 0.8])

        elif sextant == 5:
            print('5')
            await  simul_inflate(ws, [0, 0, 1])
            await asyncio.sleep(1)
            #await asyncio.sleep(0.5)
            while Glob.signBowing == True:
                await simul_inflate(ws, [0, 0, 1])
                await asyncio.sleep(0.1)
                math_bowing()

        elif sextant == 6:
            print('6')
            await simul_inflate(ws, [1, 0, 1])

async def seek(ws, sextant):
    f = 0

### ### STATE FUNCTION - OVERARCHING STRUCTURE ### ### =================================================

async def AWAKE(ws):              

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

        # print('waving is', signal_Waving())
        # print('bowing is', math_bowing())
        # print('hugging is',signal_hug(Glob.distance))
        
        if signal_Waving() and (Glob.distance < 2 and (signal_hug(Glob.distance)!=True and math_bowing()!=True and signal_tickle(Glob.distance_lhand,Glob.distance_rhand)!=True)):
            # if waving and distance > 2 and not hugging and not bowing and not tickling either hand
            f = 0   ############################################
            # print('waving')
            # await preq.waving(ws)
            
        elif math_bowing():
            # if bowing
            f = 0   ############################################
            # print('bows')
            # await preq.bow(ws, Glob.sextant)
            
        elif signal_hug(Glob.distance) and Glob.distance<2:
            # if hugging and within distance
            f = 0   ############################################
            # print('hug')
            # await hug(ws)
        
        elif signal_hug(Glob.distance)!=True and signal_tickle(Glob.distance_lhand,Glob.distance_rhand)==True:
            # if not hugging and tickling
            f = 0   ############################################
            # Glob.current_behaviour = 'tickling'
            # print('tickle')
            # await tickle(ws)
            
        elif (signal_Waving() and math_bowing() and signal_hug(Glob.distance))!= True:     
            # not waving or bowing or hugging
            f = 0   ############################################
            print('waiting')
            await waiting(ws)






############################################################################################################
##############################################   TEST  #####################################################

# async def recvpump(ws):
#     while True:
#         await ws.recv()

# async def yaught(ws):
#     while True:
#         await AWAKE(ws)

# async def test():    # testing continuously

#     async with websockets.connect(f"ws://10.20.24.10:5555/ws", ping_interval=5, ping_timeout=5) as ws:
#             while True:
#                 tasks = [                                       
#                 asyncio.ensure_future(yaught(ws)),                
#                 asyncio.ensure_future(recvpump(ws))             
#                 ]
#                 await asyncio.wait(tasks)    


# if __name__ == "__main__":
#     logging.basicConfig(
#         format="%(asctime)s %(message)s",
#         level=logging.CRITICAL #.DEBUG,
#     )

#     asyncio.run(test())     