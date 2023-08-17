


import time
import asyncio
from Glob import Glob




async def bloop(bloop_starttime, bloop_duration, target_0, target_1):        

    Glob.bloop_start_time = bloop_starttime
    bloop_end_time = bloop_starttime + bloop_duration

    def start_new_bloop():              # record starting l values

        Glob.bloop_target_0 = target_0
        Glob.bloop_target_1 = target_1

        Glob.bloop_starting_0 = list(Glob.l0)
        Glob.bloop_starting_1 = list(Glob.l1)

        for i in range(3):
            Glob.bloop_diff_0[i] = target_0[i] - Glob.bloop_starting_0[i]
            Glob.bloop_diff_1[i] = target_1[i] - Glob.bloop_starting_1[i]
        
        print('BLOOP - started new loop')






    

    if target_0 != Glob.bloop_target_0 or target_1 != Glob.bloop_target_1:          # differet target - different loop
        print('1')
        start_new_bloop()
        return

    elif target_0 == Glob.bloop_target_0 and target_1 == Glob.bloop_target_1:       # same target 

        # same target, 
        if round(Glob.bloop_start_time,2) != round(bloop_start_ref,2):
            print('start t', round(Glob.bloop_start_time, 2), '       start ref', round(bloop_start_ref, 2))
            start_new_bloop()
            return

        # same target, same loop, started earlier
        elif round(Glob.bloop_start_time, 2) == round(bloop_start_ref, 2):       

            Glob.bloop_t = time.time() - Glob.bloop_start_time

    if Glob.bloop_t >= bloop_duration:

        Glob.l0 = target_0
        Glob.l1 = target_1

        Glob.bloop_start_time = 0.0
        Glob.bloop_target_0 = [0,0,0]
        Glob.bloop_target_1 = [0,0,0]
        print('BLOOP - target reached, END')
        return
    
    elif Glob.bloop_t < bloop_duration:

        for i in range(3):

            Glob.l0[i] = Glob.bloop_starting_0[i] + ((Glob.bloop_t/bloop_duration) * Glob.bloop_diff_0[i])
            Glob.l1[i] = Glob.bloop_starting_1[i] + ((Glob.bloop_t/bloop_duration) * Glob.bloop_diff_1[i])

        print('phase = ', Glob.bloop_t/bloop_duration)
        print('starting 0' , Glob.bloop_starting_0, '                diff', Glob.bloop_diff_0)
        print('L0 = ', Glob.l0, ',   L1 = ', Glob.l1)

        return

async def yaught():
    
    Glob.t = 0
    Glob.start_time = time.time()

    Glob.l0 = [0,0,0]
    Glob.l1 = [0,0,0]

    print('start')

    while True:

        Glob.t = time.time() - Glob.start_time

        if Glob.t <= 4:
            await bloop(Glob.start_time, 3, [100,100,100], [100,100,100])
            await asyncio.sleep(0.2)

        else:
            print('end')
            return

asyncio.run(yaught())


# Why dont i just define the start and end times and do it like that. it can be all manual and controlled by Glob.t. 
# end time is just start + duration. wow im so smort