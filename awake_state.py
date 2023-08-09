### AWAKE STATE AND ALL EXCLUSIVE SUB-BEHAVIOURS GO HERE. 
### AWAKE - PERSON DETECTED BUT NOT IN INTERACTION RANGE
### EVERYTHING IN THIS FILE NEEDS TO OBEY THE 0.1 REFRESH STRUTURE WITHIN THE OVERARCHING AWAKE 


from imports import *
from Glob import Glob
from Prerequisites import *
from skelCoord import *
from decisions import *

async def awaken(ws):             # rouse from sleep. Uninterruptible until complete

    Glob.current_behaviour = 'awakening...'

    wake_type = random.choice([1,2,3,4,5])
    print(wake_type)

    async def blink(ws):                # 1
        print('blink')
        await preq.alight_ends(ws, [0,0,255], [0, 0, 0])
        await preq.simul_inflate(ws, [0.6,0.6,0.6])
        await asyncio.sleep(0.3)

        await preq.alight(ws, 0,0,0)
        await asyncio.sleep(0.3)

        await preq.alight_ends(ws, [0,0,255], [0, 0, 0])
        await preq.simul_inflate(ws, [0.8,0.8,0.8])
        await asyncio.sleep(0.3)

        await preq.alight(ws, 0,0,0)
        await asyncio.sleep(0.3)

        await preq.alight_ends(ws, [0,0,255], [0, 0, 255])
        await preq.simul_inflate(ws, [1,1,1])
        await asyncio.sleep(0.8)

    async def wink(ws):                 # 2 ~# bruh
        print('wink')
        downtime = 1.5
        down = [[0,0,0], [0,0,0]]
        await preq.flow(ws, downtime, down)
        uptime = 1.5
        up = [[30,255,30], [30,255,730]]
        await preq.flow(ws, uptime, up)
        await preq.simul_inflate(ws, [1,1,1])

    async def yawn(ws):                 # 3
        print('yawn')

        end_lights_bot = [250, 100, 0]

        await preq.simul_inflate(ws, [1,1,1])
        await preq.flow(ws, 1, [end_lights_bot, end_lights_bot])              # change colour ######################
        await preq.simul_inflate(ws, [0.6,0.6,0.6])
        await asyncio.sleep(0.5)
        
    async def morning_wood(ws):         # 4
        print('boing')
        await simul_inflate(ws, [0.1,0.1,0.1])                                  # oughh...
        await alight(ws, 0, 0, 0)
        await asyncio.sleep(2)
        await preq.reset(ws)                                   # boooiiing
        await alight_ends(ws, [255,0,255], [255,0,0])
        await asyncio.sleep(2)

    async def ready_set_go(ws):         # 5
        print('rsg')
        await alight_ends(ws, [0,0,0], [255,0,0])       # Ready
        await asyncio.sleep(0.3)
        await alight(ws, 0, 0, 0)
        await asyncio.sleep(0.3)

        await alight(ws, 255, 255, 0)       # Set
        await asyncio.sleep(0.3)
        await alight(ws, 0, 0, 0)
        await asyncio.sleep(0.3)
        
        await alight(ws, 0, 255, 0)       # Go!
        await asyncio.sleep(0.5)


    if wake_type == 1:
        await blink(ws)

    elif wake_type == 2:
        await wink(ws)

    elif wake_type == 3:
        await yawn(ws)
    
    elif wake_type == 4:
        await morning_wood(ws)

    elif wake_type == 5:    
        await ready_set_go(ws)

    elif wake_type == 6:
        pass

    print('stabilise')
    await preq.flow(ws, 0.7, [[150,80,255],[150,80,255]])
    Glob.current_state = 'AWAKE'
                        

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
        
    ########################################################################################################################################
        print('jumping is', signal_jumping())
        print('waving is', signal_Waving())
        print('bowing is', math_bowing())
       
        print('hugging is',signal_hug(Glob.distance))
        if signal_jumping()==True and signal_hug!=True:
            await preq.jumping(ws)
        
        elif signal_Waving() and (Glob.distance < 2 and (signal_hug(Glob.distance)!=True and math_bowing()!=True and signal_tickle(Glob.distance_lhand,Glob.distance_rhand and signal_jumping!=True)!=True)):
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


                r_min, r_max = 100, 150
                g_min, g_max = 0, 80
                b = 255
                
                num_pixels = 256  # Number of pixels in the gradient
                
                for i in range(10):
                    # Calculate the current position in the gradient                        
                    position = i / (num_pixels - 1)
                    
                    # Use sine functions to interpolate between R and G values
                    r = int(r_min + (r_max - r_min) * (math.sin(2 * math.pi * position) + 1) / 2)
                    g = int(g_min + (g_max - g_min) * (math.sin(2 * math.pi * position + math.pi) + 1) / 2)
                
                    await preq.alight_ends(ws,[r,g,b],[r+20,g+20,b])

        else:
            pass
            
    else:
        pass
