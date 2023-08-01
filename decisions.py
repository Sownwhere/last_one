# DECISIONS MADE BASED ON SKELETON COORDINATE READINGS. 

#############################################################
##### INCLUDE TRIED AND TESTED decision()
##### PUT ACCELERATION() ALSO HERE
##### BASICALLY ANY REACTION BASED ON MOTIONS

from imports import *
from skelCoord import *
import Prerequisites as preq
from Glob import Glob
import math



async def decision():                               # outputs state choice every 10 readings

    #global Position, finalstate, i, p, robot_pos

    radius = 1.3             # radius within which reaction occurs
    state = [0,0,0]          # transient state array - best of 3 values > output to global
    sextnt = [0,0,0]         # transient sextant array - best of 3      > output to global
    # state 1 : sleep - no one detected
    # state 2 : awake - person detected
    # state 3 : reactive - person within interaction bound
    
    while True:

        await asyncio.sleep(0.1)

        if len(Glob.Position) == 0:

            Glob.Position = [0 ,0, 0]
            
        #Else read position                 
        else:
                
            if Glob.detected == 0:          # NOBODY detected > send to globals
                
                del state[0]
                state.append(1)
                del sextnt[0]
                sextnt.append(0)        

            elif Glob.detected > 0:         # SOMEBODY detected > 
                x_lhand_diff=Glob.threedim[7][0] - Glob.robot_pos[0]
                x_rhand_diff=Glob.threedim[4][0] - Glob.robot_pos[0]
                z_lhand_diff=Glob.threedim[7][2] - Glob.robot_pos[2]
                z_rhand_diff=Glob.threedim[4][2] - Glob.robot_pos[2]

                Glob.distance_lhand = math.sqrt((x_lhand_diff**2) + (z_lhand_diff**2)) 
                Glob.distance_rhand = math.sqrt((x_rhand_diff**2) + (z_rhand_diff**2)) 


                x_diff = Glob.Position[0] - Glob.robot_pos[0]
                z_diff = Glob.Position[2] - Glob.robot_pos[2]
                
                Glob.distance = math.sqrt((x_diff**2) + (z_diff**2))  # pythagoras - distance calculation
                                
                if Glob.distance < (radius):     # if in area range

                    del state[0]
                    state.append(3) 
                    
                else:                       # if not in area range

                    del state[0]
                    state.append(2)     
                #print('state appended')

                angle = math.atan2(z_diff, x_diff)
                unprotected_sextant = ((math.degrees(angle) + 120) % 360)
                safe_sextant = math.ceil(unprotected_sextant/60)

                del sextnt[0]
                sextnt.append(safe_sextant) 
                    
        Glob.finalstate = max(state, key = state.count)         # rewrite global finalstate
        Glob.sextant = max(sextnt, key = sextnt.count)          # rewrite global sextant 
        #print('final state is', Glob.finalstate)
        #print('final sextant is', Glob.sextant)


def math_bowing():  
    
    if len(Glob.threedim)!=0:
        
        threedim = Glob.threedim
        closedistance=0.30
    
        heightknees = (threedim[8][1]+threedim[11][1])/2
        heightneck = threedim[1][1]
        
        RLknees = (-1*heightknees) + Glob.camera_pos[1]
        RLneck = (-1*heightneck) + Glob.camera_pos[1]

        #print(RLneck-RLknees)

        if  RLneck-RLknees<closedistance:
            Glob.signBowing=True
            
        else:
            Glob.signBowing=False
            
    else:
        #print('Still no-one')
        pass
    return Glob.signBowing





    
    
def signal_Jump():
    up = abs(Glob.Velocity[1])  
    Left = abs(Glob.Velocity[0])
    far = abs(Glob.Velocity[2])
    # print(up)
    # print(up)
    # print(up)
    # print(up)
    # print(up)
    
    
    if up>0.2 and (Left <0.1 and far<0.1) :
        Glob.signJump = True
    else:
        Glob.signJump = False
    #print("res",Glob.signJump)
    return Glob.signJump




# def signal_Waving():
#     if Glob.actions == 'move hand':
#         Glob.signWaving =True
#     else:
#         Glob.signWaving= False
#     return  Glob.signWaving


def signal_jumping():
    if Glob.actions ==  'jump up':
        Glob.signJump  = True
    else:
        Glob.signJump  = False
    return Glob.signJump
        

def signal_Waving():
    avvel = 0 
    for i in range(3):
        avvel = abs(Glob.Velocity[i]) +avvel
    avvel = avvel/3  
    if (Glob.l_Elbow[0]>0.4 or Glob.l_Elbow[2]>0.4 or Glob.r_Wrist[0]>0.4 or Glob.r_Wrist[2]>0.4)  and avvel<0.03 and math_bowing()!=True or Glob.actions == 'move hand' :
        Glob.signWaving =True
    else:
        Glob.signWaving= False
    return  Glob.signWaving


# def signal_Jump1():
#     l_ankle  = Glob.threedim[10]
#     r_ankle = Glob.threedim[13]
#     if l_ankle[1] > 10 and r_ankle[1] > 10:

#         #print("work")
#         Glob.signJump = True
#     else:
#         #print("hehe",l_ankle,r_ankle)

#         #print(l_ankle,r_ankle)
#         Glob.signJump = False


def signal_hug(distance):
    
    if distance <= 0.5:
 
        Glob.signhug = True
        
    else:

        Glob.signhug = False
        
    return Glob.signhug



def signal_tickle(distance_lhand,distance_rhand):
    

    if distance_lhand<= 0.36 or distance_rhand<= 0.36:

        Glob.signtickle = True
        
    else:

        Glob.signtickle = False
        
    return Glob.signtickle

        

          