### SLEEP STATE AND ALL SUB-BEHAVIOURS GO HERE. 
### SLEEPING - WHEN NOBODY IS DETECTED
### EVERYTHING IN THIS FILE NEEDS TO OBEY THE 0.1 REFRESH STRUTURE WITHIN THE OVERARCHING SLEEPING

### I expect there to be loads of problems in this. lets get testing bois
### SUPPOSED TO:
# inhale exhale snore cycle, with random colours on some inhales or exhales
# small chance of dreaming, twitching at end of breath cycle


# top colors looked good - make in/ex dreams more gentle
# p much ready to go

from imports import *
from Glob import Glob
import Prerequisites as preq

import time
import asyncio
import random
import math
import websockets, json, sys, logging


async def SLEEPING(ws):              ### ### STATE FUNCTION - OVERARCHING STRUCTURE ### ###
    
    if Glob.current_state != 'SLEEPING':
        await preq.simul_inflate(ws, [0.6, 0.6, 0.6])
        await preq.flow(ws, 1, [[0,0,0],[0,0,0]])
        await preq.simul_inflate(ws, [0.3, 0.3, 0.3])
        Glob.current_state = 'SLEEPING'

    #print("SLEEPING")
    async def sleeby():               # inhale exhale cycle
        #print("sleebin")
        volume = [0.6, 0.2]                     # max, min chamber volume
        brightness = [1, 0.1]                  # max, min brightness
        breath_time_range = [8,12]              # t range for inhale exhale
        hold_time_range = [1,3]                 # t range for breath hold
        pauses = [1.0, 1.1, 1.2, 2.0, 3.0]      # t range for pause between 
        weights = [3, 3, 2, 1, 1]                                              
        
        if Glob.current_behaviour != 'sleebing':                     # if from foreign behaviour             
            
            Glob.current_behaviour = 'sleebing'                      # new behaviour      
            Glob.start_time = time.time()                            # reset timer
            Glob.t = 0

            Glob.breath_time = random.uniform(breath_time_range[0], breath_time_range[1])
            Glob.hold_time = random.uniform(hold_time_range[0], hold_time_range[1])
            Glob.pause_time = random.choices(pauses, weights)[0]
            Glob.duration = Glob.breath_time + Glob.hold_time + Glob.pause_time     # reset duration

            Glob.dream_in = random.choices([0, 1], [7,1])[0]    # 1 in 5 dream on inhale
            Glob.dream_out = random.choices([0, 1], [7,1])[0]   # ditto exhale

        elif Glob.current_behaviour == 'sleebing':                   # within sleeb loop

            Glob.current_behaviour = 'sleebing' 
            Glob.t = time.time() - Glob.start_time

        def inhale(t):
            print('inhaling')
            t = Glob.t

            phase = math.sin(t*math.pi/Glob.breath_time)**2
            p0 = phase*(volume[0] - volume[1]) + volume[1]
            p1 = phase*(volume[0] - volume[1]) + volume[1]
            p2 = phase*(volume[0] - volume[1]) + volume[1]

            if Glob.dream_in == 1:

                R0 = phase*(random.uniform(50,255))
                G0 = phase*(random.uniform(50,255))
                B0 = phase*(random.uniform(50,255))
                R1 = phase*(random.uniform(50,255))
                G1 = phase*(random.uniform(50,255))
                B1 = phase*(random.uniform(50,255))
            
            elif Glob.dream_in == 0:

                R0 = round((phase*(brightness[0] - brightness[1]) + brightness[1])*255)
                G0 = round((phase*(brightness[0] - brightness[1]) + brightness[1])*100)
                B0 = round((phase*(brightness[0] - brightness[1]) + brightness[1])*0)
                R1 = round((phase*(brightness[0] - brightness[1]) + brightness[1])*255)
                G1 = round((phase*(brightness[0] - brightness[1]) + brightness[1])*50)
                B1 = round((phase*(brightness[0] - brightness[1]) + brightness[1])*0)

            p_in = [p0, p1, p2]
            l0_in = [R0, G0, B0]
            l1_in = [R1, G1, B1]
            print(' end of inhaling')
            return p_in, l0_in, l1_in
            
        def exhale(t):
            print('exhaling')
            t = Glob.t
            hold = Glob.hold_time

            phase = math.sin((t - hold)*math.pi/Glob.breath_time)**2
            p0 = phase*(volume[0] - volume[1]) + volume[1]
            p1 = phase*(volume[0] - volume[1]) + volume[1]
            p2 = phase*(volume[0] - volume[1]) + volume[1]

            if Glob.dream_out == 1:

                R0 = phase*(random.uniform(50,255))
                G0 = phase*(random.uniform(50,255))
                B0 = phase*(random.uniform(50,255))
                R1 = phase*(random.uniform(50,255))
                G1 = phase*(random.uniform(50,255))
                B1 = phase*(random.uniform(50,255))

            elif Glob.dream_out == 0:

                #Change colours here like the inhale
                
                R0 = round((phase*(brightness[0] - brightness[1]) + brightness[1])*255)
                G0 = round((phase*(brightness[0] - brightness[1]) + brightness[1])*100)
                B0 = round((phase*(brightness[0] - brightness[1]) + brightness[1])*0)
                R1 = round((phase*(brightness[0] - brightness[1]) + brightness[1])*255)
                G1 = round((phase*(brightness[0] - brightness[1]) + brightness[1])*50)
                B1 = round((phase*(brightness[0] - brightness[1]) + brightness[1])*0)

            p_ex = [p0, p1, p2]
            l0_ex = [R0, G0, B0]
            l1_ex = [R1, G1, B1]
            print('end of exhaling')
            return p_ex, l0_ex, l1_ex
        
        if Glob.t < Glob.duration:

            if Glob.t < Glob.breath_time/2:                               # inspire
                #print('inspire')
                Glob.p, Glob.l0, Glob.l1 = inhale(Glob.t)

            elif Glob.t < Glob.breath_time/2 + Glob.hold_time:                 # hold
                
                pass

            elif Glob.t < Glob.breath_time + Glob.hold_time:                   # expire
                #print('expire')
                Glob.p, Glob.l0, Glob.l1 = exhale(Glob.t - (Glob.breath_time/2 + Glob.hold_time))

            elif Glob.t < Glob.breath_time + Glob.hold_time + Glob.pause_time:      # pause
                
                pass

        elif Glob.t >= Glob.duration:

            Glob.current_behaviour = None
            
            yh = 0.2
            nah = 1 - yh
            Glob.dream_on = random.choices([0,1],[nah,yh])[0]


    async def dream(): 
        print('dreaming')
        #print('dreamin')
        dream_time_range = [1,1.5]
        lo = 100
        hi = 200

        if Glob.current_behaviour != 'dreaming':

            Glob.current_behaviour = 'dreaming'
            Glob.start_time = time.time()
            Glob.t = 0
            Glob.duration = random.uniform(dream_time_range)
            Glob.twitch = random.choices([0,1],[10,1])[0]
            Glob.flicker = random.choices([0,1], [2,1])[0]
        
        elif Glob.current_behaviour == 'dreaming':

            Glob.current_behaviour = 'dreaming'
            Glob.t = time.time() - Glob.start_time
        
        def electric_sheep(t):
            
            twitch = Glob.twitch
            flicker = Glob.flicker

            if twitch == 1:

                p0 = random.uniform(0.4,1)
                p1 = random.uniform(0.4,1)
                p2 = random.uniform(0.4,1)
                p_dream = [p0, p1, p2]

            elif twitch == 0:
                p_dream = Glob.p

            if flicker == 1:

                R = random.randint(lo, hi)
                G = random.randint(lo, hi)
                B = random.randint(lo, hi)
                R1 = random.randint(lo, hi)
                G1 = random.randint(lo, hi)
                B1 = random.randint(lo, hi)

            elif twitch == 0:

                R = 0.4*255
                G = 0.4*100
                B = 0
                R1 = 0.4*255
                G1 = 0
                B1 = 0
                
            l0_dream = [R, G, B]
            l1_dream = [R1, G1, B1]

            return p_dream, l0_dream, l1_dream

        if Glob.t < Glob.duration:
            Glob.p, Glob.l0, Glob.l1 = electric_sheep()

        if Glob.t >= Glob.duration:
            Glob.current_behaviour = None
            Glob.dream_on = 0

    if Glob.dream_on == 0:
        #print("go sleeb")
       
        while Glob.detected == 0:
            #print('enter sleeb')
            await sleeby()
            #print('actuate sleeb')
            await preq.simul_inflate(ws, Glob.p) 
            await preq.alight_ends(ws, Glob.l0, Glob.l1)
            await preq.asyncio.sleep(0.05)
            #print('sleeb pause')

    elif Glob.dream_on == 1:
        #print("go dream")

        while Glob.detected == 0:
            #print('enter dream')
            await sleeby()
            #await dream()
            #print('actuate dream')
            await preq.simul_inflate(ws, Glob.p)
            await preq.alight_ends(ws, Glob.l0, Glob.l1)
            await asyncio.sleep(0.05)
            #print('dream pause')
    

# async def test():    # testing continuously

#     async with websockets.connect(f"ws://10.20.24.10:5555/ws", ping_interval=5, ping_timeout=5) as ws:
#             while True:
#                 tasks = [                                       # running concurrently:
#                 asyncio.ensure_future(SLEEPING(ws)),             # camera code - outputs coordinates     
#                 asyncio.ensure_future(preq.recvpump(ws))             # clears buffer
#                 ]
#                 await asyncio.wait(tasks)    


# if __name__ == "__main__":
#     logging.basicConfig(
#         format="%(asctime)s %(message)s",
#         level=logging.CRITICAL #.DEBUG,
#     )
    
#     asyncio.run(test())               # vary tested function here
