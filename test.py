from multiprocessing import shared_memory, Process, Lock
import numpy as np

def write_to_memory(smm_name, lock):
    with lock:
        existing_smm = shared_memory.SharedMemory(name=smm_name)
        np_array = np.ndarray((100, 100, 100, 100), dtype=np.float64, buffer=existing_smm.buf)
        np_array = np.ones(shape=(100, 100, 100, 100), dtype=np.float64)
        existing_smm.close()
        
def read_from_memory(smm_name, lock):
    with lock:
        existing_smm = shared_memory.SharedMemory(name=smm_name)
        np_array = np.ndarray((100, 100, 100, 100), dtype=np.float64, buffer=existing_smm.buf)
        print(np_array[0, 0, 0, 0])  # Prints: 2.71828182846
        existing_smm.close()

if __name__ == '__main__':
    np_array = np.ones(shape=(100, 100, 100, 100), dtype=np.float64) * np.pi
    smm = shared_memory.SharedMemory(create=True, size=np_array.nbytes)
    np_array_smm = np.ndarray((100, 100, 100, 100), dtype=np.float64, buffer=smm.buf)
    np.copyto(np_array_smm, np_array)

    lock = Lock()

    p1 = Process(target=write_to_memory, args=(smm.name, lock))
    p2 = Process(target=read_from_memory, args=(smm.name, lock))

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    smm.close()
    smm.unlink()
