###  i hate myself. lets go
# hug works

from imports import *
from Glob import Glob
from Prerequisites import *
from skelCoord import *
from decisions import *

# AWAKEN - randomly choose wake up action --------------------------------------------------------------

async def awaken(ws):             # rouse from sleep. Uninterruptible until complete

    #################################################### make this two types; soft blink and yoink from top

    Glob.current_behaviour = 'awakening...' 

    wake_type = random.choices([1,2,3,4], [0.3,0.3,0.3,1])  
    wake_col = random.choice([1,2,3])       

    # wake_type = 1     ######################### testing
    # wake_col = 1      ######################### testing
    # print(wake_type)                      
    # print(wake_colour)                      

    async def rouse(ws):  


        one = [[0,0,0],[0,0,0]]
        two = [[0,0,0],[0,0,0]]
        three = [[0,0,0],[0,0,0]]

        if wake_col == 1:       # blu           
            one = [[255,255,255],[150,150,255]]   
            two = [[255,255,255],[150,150,255]]  
            three = [[0,255,255],[0,0,255]]

        elif wake_col == 2:     # green         
            one = [[255,255,255],[150,150,255]]   
            two = [[255,255,255],[150,150,255]]  
            three = [[0,255,255],[0,0,255]]

        elif wake_col == 3:     # yellow        
            one = [[255,255,255],[150,150,255]]   
            two = [[255,255,255],[150,150,255]]  
            three = [[0,255,255],[0,0,255]]
            
        await preq.simul_inflate(ws, [0.7,0.7,0.7])   
        await preq.flow(ws, 0.5, wake_colour)   

        await preq.simul_inflate(0.3,0.3,0.3)
        await preq.flow(ws, 0.5, one)

        await preq.simul_inflate(ws, [1,1,1])
        await preq.flow(ws, 0.5, two)
        await preq.flow(ws, 1, [[0,0,0],[0,0,0]])

        await preq.simul_inflate(ws, [1,1,1])
        await preq.flow(ws, 0.5, three)

    async def greet(ws):                  # ready to test #
        await preq.reset(ws)
        await preq.flow(ws, 0.5, [[500,600,0], [200,200,200]])                    
        await preq.simul_inflate(ws, [1,1,0.2])
        await preq.flow(ws, 1, [[255, 50, 255], [255,50, 255]])
        await asyncio.sleep(0.5)

    async def bloom(ws):                  # ready to test #
        print('bloom')
        await preq.simul_inflate(ws, [1,1,1])
        if wake_col == 1:   
            await preq.flow(ws, 0.7, [[100,100,600],[0,0,0]])
            await preq.flow(ws, 0.3, [[100,100,600],[0,255,100]])
        elif wake_col == 2:   
            await preq.flow(ws, 0.7, [[100,600,100],[0,0,0]])
            await preq.flow(ws, 0.3, [[100,600,100],[0,255,0]])
        elif wake_col == 3:   
            await preq.flow(ws, 0.7, [[600,600,100],[0,0,0]])
            await preq.flow(ws, 0.3, [[600,600,100],[255,255,0]])

    async def flair(ws):                # old color change - stable
        print('flair')
        await alight(ws, 0,0,0)
        await preq.simul_inflate(ws, [1,1,1])
        uptime = 1.5
        up = [[30,255,30], [30,255,730]]
        await preq.flow(ws, uptime, up)

    if wake_type == 1:
        await rouse(ws)

    elif wake_type == 2:          
        await greet(ws)

    elif wake_type == 3: 
        await bloom(ws)

    elif wake_type == 4:
        await flair(ws)
    

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

        await preq.bloop(0, Glob.patience, Glob.wait_colour[0], Glob.wait_colour[1])
        await preq.shift()

        f = 0       # do the waiting behaviour here

    elif Glob.t >= Glob.patience:       # greet 

        if Glob.initiative == 1:

            f = 0

        elif Glob.initiative == 0:
        
            f = 0                   # reset
        
# UNDIRECTED RESPONSES - responses without direction ---------------------------------------------------

async def hug(ws):      # ready to test # validate

    if Glob.current_behaviour != 'hugging':              # start hug

        Glob.current_behaviour = 'hugging'
        Glob.start_time = time.time()
        Glob.t = 0 
        Glob.patience = random.uniform(2,2.5)

        await alight_ends(ws, [255,255,255],[255,50,100])
        p0 = random.uniform(0.3,0.6)
        p1 = random.uniform(0.3,0.6)
        p2 = random.uniform(0.3,0.6)
        await preq.simul_inflate(ws, [p0, p1, p2])

        # print('hug initialised')
        return

    elif Glob.current_behaviour == 'hugging':           # hold hug
        
        Glob.current_behaviour = 'hugging'
        Glob.t = time.time() - Glob.start_time

        if Glob.t < Glob.patience:
            # print('wait')
            await asyncio.sleep(0.1)
            return

        elif Glob.t >= Glob.patience:
            # print('changing')
            await preq.bloop(Glob.patience, 2, [255,0,255],[255,0,255])
            await alight_ends(ws, Glob.l0, Glob.l1)
            await asyncio.sleep(0.05)
            return

async def tickle(ws):   # ready to test # the bloop isnt working

    if Glob.current_behaviour != 'tickle':
        
        Glob.current_behaviour = 'tickle'
        Glob.start_time = time.time()
        Glob.t = 0

        Glob.duration = 1
        await preq.alight_ends(ws, [255,255,255], [255,0,585])
        await preq.bloop(0, 0.9, [255,255,255],[255,0,910])

    elif Glob.current_behaviour == 'tickle':

        Glob.current_behaviour = 'tickle'
        Glob.t = time.time() - Glob.start_time

    if Glob.t <= 0.9:

        if Glob.t <= 0.1 or 0.3 < Glob.t <= 0.4 or 0.6 < Glob.t <= 0.7:
            p = [0.3, 0.9, 0.3]

        elif 0.1 < Glob.t <= 0.2 or 0.4 < Glob.t <= 0.6 or 0.7 < Glob.t <= 0.8:
            p = [0.9, 0.3, 0.3]

        elif 0.2 < Glob.t <= 0.3 or 0.5 < Glob.t <= 0.6 or 0.8 < Glob.t <= 0.9:
            p = [0.3, 0.3, 0.9]
        
        await alight_ends(ws, Glob.l0, Glob.l1)
        await simul_inflate(ws, p)
        await asyncio.sleep(0.05)
        return

    elif Glob.t > 0.9:
    
        Glob.current_behaviour = 'None'
        return
    
    return

async def wave(ws):     # ready to test # sort the damn motion thing

    R0 = random.uniform(0,255)
    G0 = 255
    B0 = random.uniform(0,255)

    R1 = random.uniform(0,50)
    G1 = 255
    B1 = random.uniform(0,50)

    wave_col = [[R0, G0, B0], [R1, G1, B1]]

    p0 = [1,1,0.2]
    p = random.shuffle(p0)

    await simul_inflate(ws, p)          
    await preq.flow(ws, 1, wave_col)
    await preq.reset(ws)

async def jumping(ws):

    print('jomp') 
    jomp_col = random.choice([1,2,3])

    await simul_inflate(ws,[1,1,1])

    if jomp_col == 1:       # gren

        l0 = []
        l1 = []
        L = [[],[]]

    elif jomp_col == 2:

        l0 = []
        l1 = []
        L = [[],[]]

    elif jomp_col == 3:

        l0 = []
        l1 = []
        L = [[],[]]

    await preq.alight_ends(ws, l0 ,l1)
    await preq.flow(ws, 1, L)

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

async def follow(ws, sextant):

    while True:
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

            await jumping(ws)
        
        elif signal_Waving() and (Glob.distance < 2 and 
            (signal_hug(Glob.distance)!=True and math_bowing()!=True and 
             signal_tickle(Glob.distance_lhand,Glob.distance_rhand and signal_jumping!=True)!=True)):
            
            await wave(ws)
            
        elif math_bowing():

            await bow(ws, Glob.sextant)
            
        elif signal_hug(Glob.distance) and Glob.distance<2:

            await preq.alight(ws, 255,100,100)
        
        elif signal_hug(Glob.distance)!=True and signal_tickle(Glob.distance_lhand,Glob.distance_rhand)==True:

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

        await wave(ws)

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