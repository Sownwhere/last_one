from imports import *
import Prerequisites as preq
from Glob import Glob
from multiprocessing import shared_memory, Process, Lock, Manager


def convert_to_move_hand(input_string):
    actions_1 = ['brushing teeth', 'hand waving', 'use a fan(with hand or paper)/feeling warm', 'handshaking']
    
    if input_string in actions_1:
        return 'move hand'
    else:
        return input_string

async def recive_data(actions,zed_signal_attrs, lock1,lock2):
    while True:
        
        lock2.acquire()
        try:
            if zed_signal_attrs['id1'] is not None: 

                Glob.confidence = zed_signal_attrs['confidence']
                Glob.ID = zed_signal_attrs['id1']
                Glob.Position = zed_signal_attrs['position']
                Glob.Velocity = zed_signal_attrs['velocity']
                Glob.AS = zed_signal_attrs['action_state']
                Glob.threedim = zed_signal_attrs['keypoint']
                Glob.twodim = zed_signal_attrs['keypoint_2d']
                Glob.trackingstate = zed_signal_attrs['tracking_state']
                Glob.l_Elbow = zed_signal_attrs['l_Elbow']
                Glob.r_Wrist = zed_signal_attrs['r_Wrist']
                Glob.detected = zed_signal_attrs['detected']
          
        finally:
            lock2.release()
        
 

        lock1.acquire()
        try:
            if actions:
                tmp = convert_to_move_hand(actions[0])
                Glob.actions = tmp
                
            
                print(tmp)
        finally:
            lock1.release()
            await asyncio.sleep(0.1)