# Works as desired

from imports import *
from Glob import Glob
import Prerequisites as preq

import time
import asyncio
import random
import math
import websockets, json, sys, logging


async def SLEEPING(ws):              ### ### STATE FUNCTION - OVERARCHING STRUCTURE ### ###
    
    if Glob.current_state != 'SLEEPING':        # fall asleep
        await preq.simul_inflate(ws, [0.6, 0.6, 0.6])
        await preq.flow(ws, 1, [[0,0,0],[0,0,0]])
        await preq.simul_inflate(ws, [0.3, 0.3, 0.3])
        Glob.current_state = 'SLEEPING'
        # print('drift off')

    async def sleeby():                         # inhale exhale cycle

        volume = [0.7, 0.3]                     # chamber volume ceiling/floor
        brightness = [1, 0.1]                   # light values ceiling/floor

        max_pressures = [0.9,0.8,1]
        base_colour_0 = [255,100,0]
        base_colour_1 = [255,50,0]

        breath_time_range = [8,12]              # t range for inhale exhale
        hold_time_range = [1,2]                 # t range for breath hold
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

            Glob.dreamspire = random.choices([0,1], [0.7,0.3])[0]
            Glob.R_period = random.uniform(0.1, 0.7)
            Glob.G_period = random.uniform(0.1, 0.7)
            Glob.B_period = random.uniform(0.1, 0.7)

            # print('initialise sleep')

        elif Glob.current_behaviour == 'sleebing':                   # within sleeb loop

            Glob.current_behaviour = 'sleebing' 
            Glob.t = time.time() - Glob.start_time
            pass

        dream_breath_order = [Glob.R_period, Glob.G_period, Glob.B_period]

        def inhale(t):

            t = Glob.t

            top_colours = [0,0,0]
            bot_colours = [0,0,0]

            if Glob.dreamspire == 0:

                top_colours = base_colour_0
                bot_colours = base_colour_1
                pass

            elif Glob.dreamspire == 1: 

                for i in range(3):
                    top_colours[i] = 150*math.sin(t*math.pi*dream_breath_order[i])**2 + 105
                    bot_colours[i] = 150*math.sin(t*math.pi*dream_breath_order[i])**2 + 105
                pass

            phase = math.sin(t*math.pi/Glob.breath_time)**2
            p_s = phase*(volume[0] - volume[1]) + volume[1]                    # pressure scalar
            l_s = (phase*(brightness[0] - brightness[1]) + brightness[1])      # lights scalar

            p_in = [0,0,0]
            l0_in = [0,0,0]
            l1_in = [0,0,0]

            for i in range(3):
                p_in[i] = max_pressures[i] * p_s
                l0_in[i] = top_colours[i] * l_s
                l1_in[i] = bot_colours[i] * l_s
                pass

            return p_in, l0_in, l1_in
            
        def exhale(t):

            t = Glob.t
            hold = Glob.hold_time

            top_colours = [0,0,0]
            bot_colours = [0,0,0]

            if Glob.dreamspire == 0:

                top_colours = base_colour_0
                bot_colours = base_colour_1
                pass

            elif Glob.dreamspire == 1: 

                for i in range(3):
                    top_colours[i] = 150*math.sin((t - hold)*math.pi*dream_breath_order[i])**2 + 105
                    bot_colours[i] = 150*math.sin((t - hold)*math.pi*dream_breath_order[i])**2 + 105
                pass

            phase = math.sin((t - hold)*math.pi/Glob.breath_time)**2
            p_s = phase*(volume[0] - volume[1]) + volume[1]
            l_s = (phase*(brightness[0] - brightness[1]) + brightness[1])      

            p_ex = [0,0,0]
            l0_ex = [0,0,0]
            l1_ex = [0,0,0]

            for i in range(3):
                p_ex[i] = max_pressures[i] * p_s
                l0_ex[i] = top_colours[i] * l_s
                l1_ex[i] = bot_colours[i] * l_s
                pass

            return p_ex, l0_ex, l1_ex
        
        if Glob.t < Glob.duration:                 

            if Glob.t < Glob.breath_time/2:                               # inspire
                
                # print('inspire', Glob.dreamspire)
                Glob.p, Glob.l0, Glob.l1 = inhale(Glob.t)

            elif Glob.t < Glob.breath_time/2 + Glob.hold_time:                 # hold
                
                # print('hold')
                pass

            elif Glob.t < Glob.breath_time + Glob.hold_time:                   # expire
                
                # print('expire', Glob.dreamspire)
                Glob.p, Glob.l0, Glob.l1 = exhale(Glob.t - (Glob.breath_time/2 + Glob.hold_time))


            elif Glob.t < Glob.breath_time + Glob.hold_time + Glob.pause_time:      # pause
                
                # print('pause')
                pass

        elif Glob.t >= Glob.duration:

            Glob.current_behaviour = None
            Glob.dream_on = 1
            # print('end', Glob.dream_on)
            return
            
    async def dream(): 
        
        if Glob.current_behaviour != 'dreaming':

            Glob.dream_type = random.choices([0,1,2],[0.7, 0.1, 0.2])[0]      

            if Glob.dream_type == 0:    # exit dream
                Glob.current_behaviour = None
                Glob.dream_on = 0               
                # print('exit dream')
                return   

            elif Glob.dream_type >= 0:
            
                Glob.current_behaviour = 'dreaming'
                Glob.start_time = time.time()
                Glob.t = 0

                if Glob.dream_type == 1:
                    Glob.duration = random.uniform(8,12)
                    pass

                elif Glob.dream_type == 2:
                    
                    Glob.duration = random.uniform(4,6) 

                    for i in range(3):
                        Glob.dA_0[i] = random.uniform(0,255)
                        Glob.dA_1[i] = random.uniform(0,255)
                        Glob.dB_0[i] = random.uniform(0,255)
                        Glob.dB_1[i] = random.uniform(0,255)
                        Glob.dC_0[i] = random.uniform(0,255)
                        Glob.dC_1[i] = random.uniform(0,255)
                        pass

                # print('dream initialised')
                
        elif Glob.current_behaviour == 'dreaming':

            Glob.current_behaviour = 'dreaming'
            Glob.t = time.time() - Glob.start_time

        async def electric_sheep():
            
            if Glob.dream_type == 1:               

                # print('turnover') 

                if Glob.t < Glob.duration/2:
                    await preq.bloop(Glob.duration/2, [255,255,0], [500,255,0])
                    await preq.shift(Glob.duration/2, [1,1,1])
                    await asyncio.sleep(0.05)

                elif Glob.t < Glob.duration:
                    await preq.bloop(Glob.duration/2, [0,0,0], [0,0,0])
                    await preq.shift(Glob.duration/2, [1,1,0])
                    await asyncio.sleep(0.05)


            elif Glob.dream_type == 2:

                # print('dream_sequence')
                await preq.simul_inflate(ws,[0.9,0.9,0])

                if Glob.t < Glob.duration*0.25:
                    await preq.bloop(Glob.duration/4, Glob.dA_0, Glob.dA_1)
                    await preq.alight_ends(ws, Glob.l0, Glob.l1)
                    await asyncio.sleep(0.05)
                    # print('dream_seq1')

                elif Glob.t < Glob.duration*0.5:
                    await preq.bloop(Glob.duration/4, Glob.dB_0, Glob.dB_1)
                    await preq.alight_ends(ws   Glob.l0, Glob.l1)
                    await asyncio.sleep(0.05)
                    # print('dream_seq2')

                elif Glob.t < Glob.duration*0.75:
                    await preq.bloop(Glob.duration/4, Glob.dC_0, Glob.dC_1)
                    await preq.alight_ends(ws, Glob.l0, Glob.l1)                    
                    await asyncio.sleep(0.05)
                    # print('dream_seq3')

                elif Glob.t < Glob.duration:
                    await preq.bloop(Glob.duration/4 - 0.02, [0,0,0], [0,0,0])
                    await preq.alight_ends(ws, Glob.l0, Glob.l1)
                    await asyncio.sleep(0.05)
                    # print('end dream_seq')

        if Glob.dream_type > 0:     

            if Glob.t < Glob.duration:

                await electric_sheep()

            elif Glob.t >= Glob.duration:

                Glob.current_behaviour = None
                Glob.dream_on = 0
                # print('exit dream duration spent')
                return
        
        else:
            pass


    # print('choose!')
    if Glob.dream_on == 0:

        while Glob.detected == 0 and Glob.dream_on == 0:

            await sleeby()

            await preq.simul_inflate(ws, Glob.p) 
            await preq.alight_ends(ws, Glob.l0, Glob.l1)
            await preq.asyncio.sleep(0.05)

    elif Glob.dream_on == 1:

        while Glob.detected == 0 and Glob.dream_on == 1:

            await dream()  

            await preq.simul_inflate(ws, Glob.p) 
            await preq.alight_ends(ws, Glob.l0, Glob.l1)
            await preq.asyncio.sleep(0.05)





############################################################################################################
##############################################   TEST  #####################################################

async def recvpump(ws):
    while True:
        await ws.recv()

async def yaught(ws):
    while True:
        await SLEEPING(ws)

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