from multiprocessing import shared_memory, Process, Lock
import numpy as np

def write_to_memory(smm_name, lock):
    with lock:
        existing_smm = shared_memory.SharedMemory(name=smm_name)
        np_array = np.ndarray((100, 100, 100, 100), dtype=np.float64, buffer=existing_smm.buf)
        np_array = np.ones(shape=(100, 100, 100, 100), dtype=np.float64)
        existing_smm.close()