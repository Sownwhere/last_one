


import time
import asyncio
from Glob import Glob




async def bloop(start_time, duration, target_0, target_1):      

    bloop_start_time = start_time        # wrt Glob.t. meaning seconds after Glob.st
    bloop_duration = duration
    bloop_end_time = bloop_start_time + bloop_duration

    def start_new_bloop():              # record starting L values, calculate and record diff values

        Glob.bloop_target_0 = target_0
        Glob.bloop_target_1 = target_1
        
        Glob.bloop_starting_0 = list(Glob.l0)
        Glob.bloop_starting_1 = list(Glob.l1)

        for i in range(3):
            Glob.bloop_diff_0[i] = target_0[i] - Glob.bloop_starting_0[i]
            Glob.bloop_diff_1[i] = target_1[i] - Glob.bloop_starting_1[i]
        
        print('BLOOP - started new loop')
        return

    # print('Glob t ', Glob.t, '     bloop start t', bloop_start_time)########################

    if target_0 != Glob.bloop_target_0 or target_1 != Glob.bloop_target_1:          # differet target - different loop

        start_new_bloop()
        return

    elif Glob.t <= bloop_start_time + 0.06:
        
        start_new_bloop()
        return

    elif bloop_start_time < Glob.t < bloop_end_time:

        Glob.bloop_t = time.time() - Glob.start_time - bloop_start_time

        for i in range(3):

            Glob.l0[i] = Glob.bloop_starting_0[i] + ((Glob.bloop_t/bloop_duration) * Glob.bloop_diff_0[i])
            Glob.l1[i] = Glob.bloop_starting_1[i] + ((Glob.bloop_t/bloop_duration) * Glob.bloop_diff_1[i])

        # print('phase = ', (Glob.t - start_time)/bloop_duration)
        # print('starting 0' , Glob.bloop_starting_0, '        diff', Glob.bloop_diff_0)
        prontable0 = [round(L,2) for L in Glob.l0]
        prontable1 = [round(L,2) for L in Glob.l1]
        print('L0 = ', prontable0, ',   L1 = ', prontable1)

        return

    elif Glob.t >= bloop_end_time:

        Glob.l0 = target_0                      # manual set to target
        Glob.l1 = target_1

        print('BLOOP - target reached, END')
        return


    # if target_0 != Glob.bloop_target_0 or target_1 != Glob.bloop_target_1:          # differet target - different loop
    #     print('1')
    #     start_new_bloop()
    #     return

    # elif target_0 == Glob.bloop_target_0 and target_1 == Glob.bloop_target_1:       # same target 

    #     # same target, 
    #     if round(Glob.bloop_start_time,2) != round(bloop_start_ref,2):
    #         print('start t', round(Glob.bloop_start_time, 2), '       start ref', round(bloop_start_ref, 2))
    #         start_new_bloop()
    #         return

    #     # same target, same loop, started earlier
    #     elif round(Glob.bloop_start_time, 2) == round(bloop_start_ref, 2):       

    #         Glob.bloop_t = time.time() - Glob.bloop_start_time

    # if Glob.bloop_t >= bloop_duration:

    #     Glob.l0 = target_0
    #     Glob.l1 = target_1

    #     Glob.bloop_start_time = 0.0
    #     Glob.bloop_target_0 = [0,0,0]
    #     Glob.bloop_target_1 = [0,0,0]
    #     print('BLOOP - target reached, END')
    #     return
    
    # elif Glob.bloop_t < bloop_duration:

    #     for i in range(3):

    #         Glob.l0[i] = Glob.bloop_starting_0[i] + ((Glob.bloop_t/bloop_duration) * Glob.bloop_diff_0[i])
    #         Glob.l1[i] = Glob.bloop_starting_1[i] + ((Glob.bloop_t/bloop_duration) * Glob.bloop_diff_1[i])

    #     print('phase = ', Glob.bloop_t/bloop_duration)
    #     print('starting 0' , Glob.bloop_starting_0, '                diff', Glob.bloop_diff_0)
    #     print('L0 = ', Glob.l0, ',   L1 = ', Glob.l1)

    #     return

async def yaught():
    
    Glob.t = 0
    Glob.start_time = time.time()

    Glob.l0 = [0,0,0]
    Glob.l1 = [0,0,0]

    print('START YAUGHT')

    while True:

        Glob.t = time.time() - Glob.start_time

        if Glob.t <= 3.1:
            await bloop(0, 3, [100,100,100], [100,100,100])
            await asyncio.sleep(0.05)

        else:
            Glob.t = 0
            Glob.start_time = time.time()

            Glob.l0 = [0,0,0]
            Glob.l1 = [0,0,0]

asyncio.run(yaught())


# Why dont i just define the start and end times and do it like that. it can be all manual and controlled by Glob.t. 
# end time is just start + duration. wow im so smort