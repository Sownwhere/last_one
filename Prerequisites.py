# PREREQUISITE FUNCTIONS - BUILDING BLOCKS FOR OTHER OPERATIONS 

from asynchat import async_chat
from imports import *
import asyncio
from Glob import Glob
from decisions import *

# Json cmd ---------------------------------------------------------------------------------------------------------

async def _send_cmd(ws, dstnode, msgtype, data):    # send cmd to vine
    await ws.send(json.dumps(dict(
        msgtype = msgtype,
        dstnode = dstnode,
        data = data,
    )))

# Recvpump - buffer clear ------------------------------------------------------------------------------------------

async def recvpump(ws):
    """Empty the recv buffer, doing nothing with the messages."""
    while True:
        await ws.recv()

# Vine inflation control ------------------------------------------------------------------------------------------

async def inflate(ws, chamber, pressure):           # assign pressure to chamber

    # set chamber c to pressure (0-1)
    if not (0 <= pressure <= 1):
        raise ValueError("Pressure should be a value between 0 and 1")

    if not (0 <= chamber <= 2):
        raise ValueError("Chamber should be a value between 0 and 2")

    await _send_cmd(ws, chamber+2, "targetdrive", pressure*1.4-0.2)  # node numbers are offset from chamber numbers by 2

async def simul_inflate(ws, p):                     # simultaneously inflate all chambers to desired pressure
    
    c0 = asyncio.create_task(inflate(ws, 0, p[0]))
    c1 = asyncio.create_task(inflate(ws, 1, p[1]))
    c2 = asyncio.create_task(inflate(ws, 2, p[2]))
    await c0
    await c1
    await c2
    await asyncio.sleep(0.1)
    Glob.p = p

# Vine light control -----------------------------------------------------------------------------------------------

async def alight(ws, r,g,b):                        # set LEDs on
    # RGB colours range 0 ~ 255(0xff)
    await _send_cmd(ws, 0, "rgb", [int(g),int(r),int(b),0])
    await _send_cmd(ws, 0, "rgb", [int(g),int(r),int(b),1])
    lights = [r, g, b]
    Glob.l0 = lights
    Glob.l1 = lights

async def alight_ends(ws, l0, l1):              # 0 top, 1 bottom, [R,G,B]
    # send lights to end of vine - addr 0 top, addrs 1 bottom
    await _send_cmd(ws, 0, "rgb", [int(l0[1]),int(l0[0]),int(l0[2]),0])
    await _send_cmd(ws, 0, "rgb", [int(l1[1]),int(l1[0]),int(l1[2]),1])
    Glob.l0 = l0
    Glob.l1 = l1

# Reset functions ---------------------------------------------------------------------------------------------------

async def reset(ws):                                # reset all chambers to 1

    p = [1,1,1]
    await simul_inflate(ws, p)

async def relight(ws):                              # set lights to full

    await alight(ws, 255,255,255)

async def full_reset(ws):                           # both
    await reset(ws)
    await relight(ws)
    await asyncio.sleep(1)

# Transitions ------------------------------------------------------------------------------------------------------

# LIGHTS : flow() over short period - uninterruptible

async def flow(ws, flow_duration, target_lights):       # Uninterruptible; short term, only lights ### this works ###

    start_top = Glob.l0
    start_bot = Glob.l1

    target_top = target_lights[0]
    target_bot = target_lights[1]

    refresh_rate = 20                       # 1/0.05 seconds
    num_steps = int(flow_duration*refresh_rate)

    increment_top = [(target_val - start_val) / num_steps for target_val, start_val in zip(target_top, start_top)]
    increment_bot = [(target_val - start_val) / num_steps for target_val, start_val in zip(target_bot, start_bot)]

    for step in range(num_steps):

        Glob.l0 = [start_val + step * inc for start_val, inc in zip(start_top, increment_top)]
        Glob.l1 = [start_val + step * inc for start_val, inc in zip(start_bot, increment_bot)]

        await alight_ends(ws, Glob.l0, Glob.l1)
        await asyncio.sleep(1/refresh_rate)

    Glob.l0 = target_lights[0]
    Glob.l1 = target_lights[1]

    await alight_ends(ws, Glob.l0, Glob.l1)

# LIGHTS : bloop() over long period - interruptible

async def bloop(bloop_duration, target_0, target_1, refresh_rate):             # Interruptible. over long period 

    bloop_refresh = refresh_rate
    n = bloop_duration*bloop_refresh

    def start_new_bloop():

        Glob.bloop_start_t = time.time()
        Glob.bloop_t = 0

        Glob.bloop_target_0 = target_0
        Glob.bloop_target_1 = target_1

        Glob.bloop_starting_0 = list(Glob.l0)
        Glob.bloop_starting_1 = list(Glob.l1)

        for i in range(3):
            Glob.bloop_diff_0[i] = target_0[i] - Glob.bloop_starting_0[i]
            Glob.bloop_diff_1[i] = target_1[i] - Glob.bloop_starting_1[i]
        
        print('BLOOP - started new loop')

    if target_0 == Glob.bloop_target_0 and target_1 == Glob.bloop_target_1:
        # if same target

        if time.time() == Glob.bloop_start_t:
            # start time is now

            start_new_bloop()
            await asyncio.sleep(0.01)

        else:
            # start time was earlier

            Glob.bloop_t = time.time() - Glob.bloop_start_t
            #print('continue existing loop')

    elif target_0 != Glob.bloop_target_0 or target_1 != Glob.bloop_target_1:
        # if different target

        start_new_bloop()
        await asyncio.sleep(0.01)

    if Glob.bloop_t >= bloop_duration:

        print('BLOOP - target reached, END')
        Glob.l0 = target_0
        Glob.l1 = target_1

        Glob.bloop_start_t = 0.0
        Glob.bloop_target_0 = [0,0,0]
        Glob.bloop_target_1 = [0,0,0]

        return
    
    elif Glob.bloop_t < bloop_duration:

        for i in range(3):

            Glob.l0[i] = Glob.bloop_starting_0[i] + ((Glob.bloop_t/bloop_duration) * Glob.bloop_diff_0[i])
            Glob.l1[i] = Glob.bloop_starting_1[i] + ((Glob.bloop_t/bloop_duration) * Glob.bloop_diff_1[i])

        # print('phase = ', Glob.bloop_t/bloop_duration)
        # print('L0 = ', Glob.l0, ',   L1 = ', Glob.l1)

        return
    
# MOTION : shift() over long period - interruptible

async def shift(shift_duration, target_p, refresh_rate):             # Interruptible. over long period 

    shift_refresh = refresh_rate
    n = shift_duration*shift_refresh

    def start_new_shift():

        Glob.shift_start_t = time.time()
        Glob.shift_t = 0

        Glob.shift_target = target_p

        Glob.shift_starting_p = list(Glob.p)

        for i in range(3):
            Glob.shift_diff[i] = target_p[i] - Glob.shift_starting_p[i]
        
        print('SHIFT - started new loop')
        return

    if target_p == Glob.shift_target:
        # if same target

        if time.time() == Glob.shift_start_t:
            # start time is now

            start_new_shift()
            await asyncio.sleep(0.01)

        else:
            # start time was earlier

            Glob.shift_t = time.time() - Glob.shift_start_t

    elif target_p != Glob.shift_target:
        # if different target

        start_new_shift()
        await asyncio.sleep(0.01)

    if Glob.shift_t >= shift_duration:

        print('SHIFT - target reached, END')
        Glob.p = target_p

        Glob.shift_start_t = 0.0
        Glob.shift_target = [0,0,0]

        return
    
    elif Glob.shift_t < shift_duration:

        for i in range(3):

            Glob.p[i] = Glob.shift_starting_p[i] + ((Glob.shift_t/shift_duration) * Glob.shift_diff[i])

        # print('phase = ', Glob.shift_t/shift_duration)
        # print('p = ', Glob.p)

        return

# BEHAVIOURS FOR AWAKE STATE ########################################################################################################################

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


async def RLRGB(ws):
    # Define initial state and action space#
    global globalRGB 
    rgbstate = globalRGB
    #rgbstate = [random.randint(0,255), random.randint(0,255), random.randint(0,255)]  # initial RGB values for the color
    actions = ['+R', '-R', '+G', '-G', '+B', '-B']  # increase or decrease R, G, or B value

    # Define Q-table with initial values
    q_table = {}

    # Define learning rate and discount factor
    learning_rate = 0.1
    discount_factor = 0.99

    # Define exploration rate and minimum exploration rate
    exploration_rate = 1
    min_exploration_rate = 0.01
    exploration_decay_rate = 0.001

    #while True:
    # Choose action based on exploration vs exploitation
    if random.uniform(0, 1) < exploration_rate:
        action = random.choice(actions)
    else:
        q_values = q_table.get(str(rgbstate), {})
        if len(q_values) == 0:
            action = random.choice(actions)
        else:
            action = max(q_values.items(), key=lambda x: x[1])[0][-2:]

    # Take action and observe new rgbstate
    if action == '+R':
        new_rgbstate = [min(rgbstate[0]+20, 255), rgbstate[1], rgbstate[2]]
    elif action == '-R':
        new_rgbstate = [max(rgbstate[0]-20, 0), rgbstate[1], rgbstate[2]]
    elif action == '+G':
        new_rgbstate = [rgbstate[0], min(rgbstate[1]+20, 255), rgbstate[2]]
    elif action == '-G':
        new_rgbstate = [rgbstate[0], max(rgbstate[1]-20, 0), rgbstate[2]]
    elif action == '+B':
        new_rgbstate = [rgbstate[0], rgbstate[1], min(rgbstate[2]+20, 255)]
    else:
        new_rgbstate = [rgbstate[0], rgbstate[1], max(rgbstate[2]-20, 0)]
    y1 = Glob.person1[0]

    # Update Q-table based on feedback
    if y1 > 0:
        reward = -1
    else:
        reward = 1

    old_q_value = q_table.get(str(rgbstate), {}).get(action, 0)
    q_table.setdefault(str(rgbstate), {})[action] = old_q_value + learning_rate * (reward + discount_factor * max(q_table.get(str(new_rgbstate), {}).values(), default=0) - old_q_value)

    # Update rgbstate
    rgbstate = new_rgbstate

    #Output RGB to go to robot

    R = rgbstate[0]
    G = rgbstate[1]
    B = rgbstate[2]
    globalRGB = rgbstate
    #print(rgbstate)
    await asyncio.sleep(0.1)
    await alight(ws,R, G, B)


    # Decay exploration rate
    exploration_rate = max(min_exploration_rate, exploration_rate * (1 - exploration_decay_rate))


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

        Glob.current_behaviour = 'waiitng'
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
        
