### 11 SEPTEMBER 2023 
### TESTING SPROUT FOR DECREASED RANGES OF MOTION

# For all technical audiences: this is an entirely self contained file. 
# gonna have all imports/globals/dependencies in here, to isolate the problem

import asyncio, math, time
import websockets, json, sys, logging

############################################################################
'''
    For the patient individual kindly testing this for us:
    INSTRUCTIONS:

    1 . please change the value of CONTROL (currently 0) to 
    another value between 1 and 9 on instruction.'''


                          #    
                        ###     THIS THOU MUST CHANGETH
                      #####
                    #############################
                  ################################
CONTROL = 1     ###################################
                  ################################
                    #############################
                      #####
                        ###           NAUGHT ELSE
                          #

'''
   2. File -> Save     or      File -> Save All

   3. Click the little play button on the upper right corner to run the script
   
   4. Upon completion or if needed, the process can be interrupted by clicking
      inside the terminal and hitting CTRL + C                             '''

##############################################################################
# For office use only

# 'Firmware' - necessary prerequisites ---------------------------------------

async def _send_cmd(ws, dstnode, msgtype, data):
    # send json command to vine
    await ws.send(json.dumps(dict(
        msgtype = msgtype,
        dstnode = dstnode,
        data = data,
    )))

async def recvpump(ws):
    # empty recv buffer
    while True:
        await ws.recv()

# Vine basic inflation control -----------------------------------------------------

async def inflate(ws, chamber, pressure):   # previously known as 'send_chamber_drive
                                            # renamed for convention and ease of use

    # Sends a pressure value (0 - 1) to the designated chamber

    if not (0 <= pressure <= 1):
        raise ValueError('invalid pressure: 0 < p < 1')

    if not (0 <= chamber <= 2):
        raise ValueError('invalid chamber: 0,1,2')

    await _send_cmd(ws, chamber+2, "targetdrive", pressure*1.4-0.2)  # node numbers are offset from chamber numbers by 2


# Vine modified inflation control ---------------------------------------------------------

async def simul_inflate(ws, p):             # simultaneously inflate all chambers to desired pressure
                                            # eliminated need to call loop for 3 each time
    
    c0 = asyncio.create_task(inflate(ws, 0, p[0]))
    c1 = asyncio.create_task(inflate(ws, 1, p[1]))
    c2 = asyncio.create_task(inflate(ws, 2, p[2]))
    await c0
    await c1
    await c2

# Actions - original, unmodified ----------------------------------------------------------

async def stress(ws):
    """Flap the vine, deflating and inflating all chambers every 2 secs"""
    while True:
        for c in range(0,3):
            await inflate(ws, c, 0)
        await asyncio.sleep(2)

        for c in range(0,3):
            await inflate(ws, c, 1)
        await asyncio.sleep(2)

async def stress_simul(ws):
    # stress() using simul_inflate()
    while True:
        await simul_inflate(ws, [0,0,0])
        await asyncio.sleep(2)

        await simul_inflate(ws, [1,1,1])
        await asyncio.sleep(2)

async def alternate(ws):
    """Alternately deflate each chamber, moving the vine in a triangular way."""
    low = 0.3
    while True:
        for c in range(0,3):
            # Make this chamber's drive low
            await inflate(ws, c, low)
            await asyncio.sleep(3)
            # Reset to full
            await inflate(ws, c, 1)

async def circle(ws):       # lobotomised to remove the lights aspect
    """Move smoothly in a circular-ish way, while fading LEDs"""
    while True:

        period = 15
        drives = [1.0,1.0,1.0]

        t = time.time()

        # remainder = (t % period)/period         # 0 to 1
        # phase = remainder * 2 * math.pi         # 0 to 2 pi
        chamber = int(3 * (t % period)/period)  # 0 to 2

        drives[chamber] = (t%(period/3.0)) / (period/3.0)

        for c in range(0,3):   
            await inflate(ws, c, drives[c])
        
        # red = 127+(127*math.sin(phase))
        # green = 127+(127*math.sin(phase+2*math.pi/3))
        # blue = 127+(127*math.sin(phase+2*2*math.pi/2))
        
        # await send_leds(ws, red, green, blue)
       
        await asyncio.sleep(0.2)

async def circle_simul(ws):

    while True: 

        period = 15
        drives = [1.0,1.0,1.0]

        t = time.time()

        chamber = int(3 * (t % period)/period)  # 0 to 2

        drives[chamber] = (t%(period/3.0)) / (period/3.0)

        await simul_inflate(ws, drives)
        
        await asyncio.sleep(0.2)

async def main():

    i = CONTROL

    async def countdown():
        print('3...')
        await asyncio.sleep(1)
        print('2...')
        await asyncio.sleep(1)
        print('1...')
        await asyncio.sleep(1)

    if i == 0:        # ==============================================================================================      
        '''Scenario 0: Using the original command structure with inputs'''
            
        if len(sys.argv) != 3:
            print(f"Usage: {sys.argv[0]} <ip of creature> <command>", file=sys.stderr)
            sys.exit(1)
        async with websockets.connect(f"ws://{sys.argv[1]}:5555/ws", ping_interval=5, ping_timeout=5) as ws:
            cmd = sys.argv[2]
            if cmd not in globals():
                raise Exception("Bad command")

            # Run the command and recvpump concurrently. Recvpump is needed even though we
            # don't do anything with received messages to keep the recv buffer from filling
            # up, which causes us to stop receiving PONGs and thus timing out.

            await asyncio.gather(
                globals()[cmd](ws),
                recvpump(ws),
            )

    else:       # perform a countdown
        print('Scenario', CONTROL, ',   Starting ...')
        await asyncio.sleep(0.5)

        if i == 1:    # ==============================================================================================
            
            async def action(ws):
                print("expected behaviour: 'STRESS'")
                await asyncio.sleep(0.5)
                print("'Flap the vine, deflating and inflating all chambers every 2 secs'")
                await asyncio.sleep(0.5)
                await countdown()

                await stress(ws)

            async with websockets.connect(f"ws://10.20.24.10:5555/ws", ping_interval=5, ping_timeout=5) as ws:
                
                while True: 
                    tasks = [
                    asyncio.ensure_future(action(ws)),
                    asyncio.ewnsure_future(recvpump(ws))
                    ]

                    await asyncio.wait(tasks)

        elif i == 2:  # ==============================================================================================
           
            async def action(ws):
                print("expected behaviour: 'ALTERNATE'")
                await asyncio.sleep(0.5)
                print("'Alternately deflate each chamber, moving the vine in a triangular way.'")
                await asyncio.sleep(0.5)
                await countdown()

                await alternate(ws)    

            async with websockets.connect(f"ws://10.20.24.10:5555/ws", ping_interval=5, ping_timeout=5) as ws:
                
                while True: 
                    tasks = [
                    asyncio.ensure_future(action(ws)),
                    asyncio.ensure_future(recvpump(ws))
                    ]

                    await asyncio.wait(tasks)

        elif i == 3:  # ==============================================================================================
            
            async def action(ws):
                print("expected behaviour: 'CIRCLE'")
                await asyncio.sleep(0.5)
                print("'Move smoothly in a circular-ish way, while fading LEDs'")
                await asyncio.sleep(0.5)
                await countdown()

                await circle(ws) 

            async with websockets.connect(f"ws://10.20.24.10:5555/ws", ping_interval=5, ping_timeout=5) as ws:
                
                while True: 
                    tasks = [
                    asyncio.ensure_future(action(ws)),
                    asyncio.ensure_future(recvpump(ws))
                    ]

                    await asyncio.wait(tasks)

        elif i == 4:  # ==============================================================================================
            
            async def action(ws):
                print("stress - check simul")
                await asyncio.sleep(0.5)
                await countdown()

                await stress_simul(ws) 

            async with websockets.connect(f"ws://10.20.24.10:5555/ws", ping_interval=5, ping_timeout=5) as ws:
                
                while True: 
                    tasks = [
                    asyncio.ensure_future(action(ws)),
                    asyncio.ensure_future(recvpump(ws))
                    ]

                    await asyncio.wait(tasks)

        elif i == 5:  # ==============================================================================================
            
            async def action(ws):
                print("circle - check simul")
                await asyncio.sleep(0.5)
                await countdown()

                await circle_simul(ws) 

            async with websockets.connect(f"ws://10.20.24.10:5555/ws", ping_interval=5, ping_timeout=5) as ws:
                
                while True: 
                    tasks = [
                    asyncio.ensure_future(action(ws)),
                    asyncio.ensure_future(recvpump(ws))
                    ]

                    await asyncio.wait(tasks)

if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s %(message)s",
        level=logging.CRITICAL #.DEBUG,
    )
    asyncio.run(main())