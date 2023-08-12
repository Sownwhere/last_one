###  i hate myself. lets go
# hug works

from imports import *
from Glob import Glob
from Prerequisites import *
from skelCoord import *
from decisions import *

# AWAKEN - randomly choose wake up action --------------------------------------------------------------

async def awaken(ws):             # rouse from sleep. Uninterruptible until complete

    Glob.current_behaviour = 'awakening...' 

    wake_type = random.choice([1,2,3,4,5])  
    wake_col = random.choice([1,2,3])       
    wake_colour = [[0,0,0],[0,0,0]]         

    if wake_col == 1:       # blu           
        wake_colour = [[255,255,255],[150,150,255]]     

    elif wake_col == 2:     # green         
        wake_colour = [[255,255,255],[100,255,200]]     

    elif wake_col == 3:     # yellow        
        wake_colour = [[255,255,255],[200,255,100]]     

    # print(wake_type)                      
    # print(wake_colour)                      

    async def rouse():  
        await preq.simul_inflate(ws, [1,1,1])   
        await preq.alight_ends(ws, [255,255,255],[0,0,0])
        await preq.flow(ws, 0.5, wake_colour)   

    async def greet():                         
        await asyncio.sleep()
        await preq.alight_ends(ws, [])

    async def bloom():
        print('bloom')

    async def bloom(ws):                 # 2 ~# bruh     # colour change one atm
        print('bloom')
        downtime = 0.5
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
        Glob.duration = random.uniform ()
        Glob.initiative = random.choices([0,1], [2,1])

        print('patience', Glob.patience, 'initiative', Glob.initiative)

        R0 = random.uniform(0,255)
        G0 = random.uniform(0,255)
        B0 = random.uniform(0,255)

        R1 = random.uniform(0,255)
        G1 = random.uniform(0,255)
        B1 = random.uniform(0,255)

        Glob.wait_colour = [[R0, G0, B0],[R1, G1, B1]]
        Glob.wait_pos = 0

        print('initialise wait')

    elif Glob.current_behaviour == 'waiting':

        Glob.current_behaviour = 'waiting'
        Glob.t = time.time() - Glob.start_time

    if Glob.t < Glob.patience:

        await preq.bloop(Glob.patience, Glob.wait_colour[0], Glob.wait_colour[1], 0.01)
        await preq.shift()

        f = 0       # do the waiting behaviour here

    elif Glob.t >= Glob.patience:       # greet 

        if Glob.initiative == 1:

            f = 0

        elif Glob.initiative == 0:
        
            f = 0                   # reset
        
# UNDIRECTED RESPONSES - responses without direction ---------------------------------------------------

async def hug(ws):                                                  ######################## 'TEST TEST TEST' ######################    
    print("huggin")

    if Glob.current_behaviour != 'hugging':              # start hug

        Glob.current_behaviour = 'hugging'
        Glob.start_time = time.time()
        Glob.t = 0 
        Glob.patience = random.uniform(2,3)

        await alight_ends(ws, [255,255,255],[255,50,100])
        p0 = random.uniform(0.4,0.7)
        p1 = random.uniform(0.4,0.7)
        p2 = random.uniform(0.4,0.7)
        await preq.simul_inflate(ws, [p0, p1, p2])

        print('hug initialised')

    elif Glob.current_behaviour == 'hugging':           # hold hug
        
        Glob.current_behaviour = 'hugging'
        Glob.t = time.time() - Glob.start_time

        if Glob.t < Glob.patience:
            print('wait')
            await asyncio.sleep(0.1)
            pass

        elif Glob.t >= Glob.patience:

            print('changing')
            await preq.bloop(3, [255,0,255],[255,0,255], 0.05)
            await alight_ends(ws, Glob.l0, Glob.l1)
            await asyncio.sleep(0.05)

async def tickle(ws):

    p0 = random.uniform([0.4,1])
    p1 = random.uniform([0.4,1])
    p2 = random.uniform([0.4,1])          
    await alight_ends(ws, [255,255,255], [255,0,585])
    await preq.flow(ws, 1, [[255,255,255],[255,0,910]])

async def waving(ws):
   
    await simul_inflate(ws,[1,0.3,0.3])
    await preq.alight()
    await preq.flow(ws, 1, )
    
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
        
async def jumping(ws):
    print('jomp') 
    jomp_col = random.choice([1,2,3])

    await simul_inflate(ws,[1,1,1])
    if jump_col == 1:
        f = 0

    await preq.alight

# DIRECTED RESPONSES - responses based on relative position --------------------------------------------

async def bow(ws, sextant):
    
    signBowing = Glob.signBowing
    
    await reset(ws)         ################# testing
    await asyncio.sleep(3)  ################# testing

    # if signBowing == True:
    while True:
        await alight_ends(ws,[255,0,255],[255,0,255])
        #await alight_ends(ws,[0,255,0],[0,255,0])
        #print('choosing 1 to 6')

        if sextant == 0:
            print('0')
            pass
    
        elif sextant == 1 or sextant == 2:
            print('first third')
            await preq.simul_inflate(ws, [1,1,0])

        elif sextant == 3 or sextant == 4:
            print('second third')
            await preq.simul_inflate(ws, [0,1,1])

        elif sextant == 5 or sextant == 6:
            print('third third')
            await preq.simul_inflate(ws, [1,0,1])

            
        # elif sextant == 1:                    # radially; 0 = reach towards chamber 0
        #     print('1')
        #     await simul_inflate(ws, [1, 0, 0])
        #     #await asyncio.sleep(0.5)
        #     await asyncio.sleep(1)
        #     while Glob.signBowing==True :
        #         await simul_inflate(ws, [0.1, 0.4, 0.4])
        #         await asyncio.sleep(0.1)
        #         math_bowing()

        # elif sextant == 2:
        #     print('2')
        #     await simul_inflate(ws, [1, 1, 0.2])

        # elif sextant == 3:
        #     print('3')
        #     await  simul_inflate(ws, [0, 1, 0])
        #     await asyncio.sleep(1.2)
        #     while Glob.signBowing == True :
        #         await simul_inflate(ws, [0.6, 0.0, 0.7])
        #         await asyncio.sleep(0.1)
        #         math_bowing()

        # elif sextant == 4:
        #     print('4')
        #     await simul_inflate(ws, [0.1, 0.8, 0.8])

        # elif sextant == 5:
        #     print('5')
        #     await  simul_inflate(ws, [0, 0, 1])
        #     await asyncio.sleep(1)
        #     #await asyncio.sleep(0.5)
        #     while Glob.signBowing == True:
        #         await simul_inflate(ws, [0, 0, 1])
        #         await asyncio.sleep(0.1)
        #         math_bowing()

        # elif sextant == 6:
        #     print('6')
        #     await simul_inflate(ws, [1, 0, 1])

        

async def seek(ws, sextant):

    f = 0

### ### STATE FUNCTION - OVERARCHING STRUCTURE ### ### =================================================

async def AWAKE(ws):              

    global current_state, current_behaviour
    global start_time, t, duration
    global p, l0, l1

    if Glob.current_state != 'AWAKE':

        await awaken(ws)

        Glob.current_state == 'AWAKE'

    elif Glob.current_state == 'AWAKE':    
        
        print('jumping is', signal_jumping())
        print('waving is', signal_Waving())
        print('bowing is', math_bowing())
        print('hugging is',signal_hug(Glob.distance))

        if signal_jumping()==True and signal_hug!=True:         

            await preq.jumping(ws)
        
        elif signal_Waving() and (Glob.distance < 2 and 
            (signal_hug(Glob.distance)!=True and math_bowing()!=True and 
             signal_tickle(Glob.distance_lhand,Glob.distance_rhand and signal_jumping!=True)!=True)):
            
            Glob.current_behaviour = 'waving'
            await preq.waving(ws)
            
        elif math_bowing():

            Glob.current_behaviour = 'bowing'
            await preq.bow(ws, Glob.sextant)
            
        elif signal_hug(Glob.distance) and Glob.distance<2:

            Glob.current_behaviour = 'hugging'
            await preq.alight(ws, 255,100,100)
        
        elif signal_hug(Glob.distance)!=True and signal_tickle(Glob.distance_lhand,Glob.distance_rhand)==True:

            Glob.current_behaviour = 'tickling'
            await tickle(ws)
            
        elif (signal_Waving() and math_bowing() and signal_hug(Glob.distance))!= True:            # more variety

            interesting_actions = ['hand waving', 'pointing to something with finger','clapping', 
                                   'put the palms together', 'rub two hands together', 'brushing teeth', 
                                   'brushing hair', 'touch head (headache)', 'touch chest (stomachache/heart pain)', 
                                   'touch neck (neckache)']

            if Glob.actions in interesting_actions:

                await preq.alight(ws, 130,240,20)

            else:

                Glob.current_behaviour = 'waiting'
                print('waiting')
                await preq.reset(ws) 


############################################################################################################
##############################################   TEST  #####################################################

async def recvpump(ws):
    while True:
        await ws.recv()

async def yaught(ws):
    await preq.full_reset(ws)
    await asyncio.sleep(2)
    while True:

        await hug(ws)


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