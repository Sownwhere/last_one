import skelCoord
import stgcnpp
import numpy as np
from multiprocessing import shared_memory, Process, Lock, Manager
from camera_test import *
import asyncio

def main_function_process(actions,zed_signal_attrs, lock1,lock2):
    asyncio.run(main_functions(actions,zed_signal_attrs, lock1,lock2))

# 在进程中启动



if __name__ == '__main__':

    frame=20
    num_keypoint =17
    dim_keypoint = 2
    
    with Manager() as manager:
        #smm for action lable
        actions = manager.list()
        #smm for skeleton data 
        np_array = np.zeros(shape=(1, frame, num_keypoint, dim_keypoint), dtype=np.float64) 
        smm = shared_memory.SharedMemory(create=True, size=np_array.nbytes)
        np_array_smm = np.ndarray((1, frame, num_keypoint, dim_keypoint), dtype=np.float64, buffer=smm.buf)
        np.copyto(np_array_smm, np_array)
        
        # Initialize zed_signal attributes as a manager dict
        zed_signal_attrs = manager.dict({
            'confidence': None,
            'id1': None,
            'position': [],
            'velocity': None,
            'action_state': None,
            'keypoint': None,
            'keypoint_2d': None,
            'tracking_state': [],
            'l_Elbow': [0,0,0],
            'r_Wrist': [0,0,0],
            'detected':None
        })
        
        lock = Lock()  #for the skeleton date
        lock1 = Lock() #for the action label
        lock2=  Lock() #for the zed_signal

        # pass zed_signal_attrs as an argument
        p0 = Process(target=skelCoord.SkelCoord, args=(smm.name, actions, zed_signal_attrs, lock, lock1, lock2))
        p1 = Process(target=main_function_process, args=(actions,zed_signal_attrs, lock1,lock2))
        p2 = Process(target=stgcnpp.main, args=(smm.name, actions, zed_signal_attrs, lock, lock1, lock2))
        
        p0.start()
        p1.start()
        p2.start()

        p0.join()
        p1.join()
        p2.join()

        smm.close()
        smm.unlink()
