
from imports import *
from Prerequisites import *
import time
from multiprocessing import shared_memory
import winsound
freq=1000
dur=20

class action__recognition():
    frame_num = 20
    keypoints = 17
    dim= 2
    count = 0
    count_to_save=1
    zeros_array = np.zeros((keypoints,dim))
    
    
def create_array(smm_name,lock):
    # 创建空的三维数组
    
    bodyarry = np.zeros((action__recognition.frame_num,action__recognition.keypoints , action__recognition.dim))  
    action__recognition.count =0
    with lock:
            existing_smm = shared_memory.SharedMemory(name=smm_name)
            np_array = np.ndarray((1, 20, 17, 2), dtype=np.float64, buffer=existing_smm.buf)
            np_array[:]=bodyarry
            existing_smm.close()
    return bodyarry
    
    
def write_date(smm_name,lock,bodyarry):
    with lock:
        existing_smm = shared_memory.SharedMemory(name=smm_name)
        np_array = np.ndarray((1, 20, 17, 2), dtype=np.float64, buffer=existing_smm.buf)
        np_array[:]=bodyarry
        existing_smm.close()
def coco18_translate_coco17(array):
    #delete the neck
    new_array = np.empty((17, 2))
      
    new_array[0]=array[0]  # nose
    new_array[1]=array[15] # left_eye
    new_array[2]=array[14]  #right_eye
    new_array[3]=array[17]  #left_ear
    new_array[4]=array[16]  #right_ear
    new_array[5]=array[5]   #left_shoulder
    new_array[6]=array[2]   #right_shoulder
    new_array[7]=array[6]   #left_elbow
    new_array[8]=array[3]   #right_elbow
    new_array[9]=array[7]   #left_wrist
    new_array[10]=array[4]  #right_wrist
    new_array[11]=array[11] # left_hip
    new_array[12]=array[8]  # right_hip
    new_array[13]=array[12] #left_knee
    new_array[14]=array[9]  # right_knee
    new_array[15]=array[13] #left_ankle
    new_array[16]=array[10]  #right_ankle
    return new_array

def add_item(smm_name,lock,twodim,bodyarry):
    tmp = coco18_translate_coco17(twodim)
    # print(len(tmp))              

    if action__recognition.count >=action__recognition.frame_num:
        # print("well")
        bodyarry= bodyarry[1:]
        action__recognition.count = 20
        bodyarry =np.concatenate((bodyarry, [tmp]), axis=0)
        #store the bodyarry into smm
        write_date(smm_name,lock,bodyarry)
    else:
        bodyarry[action__recognition.count]= np.copy(tmp)
        action__recognition.count = 1 +action__recognition.count
        print("fweg",action__recognition.count)
        write_date(smm_name,lock,bodyarry)
    return bodyarry

import numpy as np

# def delete_item(smm_name,bodyarry, lock): 
#     action__recognition.count = action__recognition.count - 1   
#     if action__recognition.count >= 0:
#         tmp = 19 - action__recognition.count
#         bodyarry[0][tmp] = np.zeros_like(bodyarry[0][tmp])
#         print(action__recognition.count)
#         # print(bodyarry[0][tmp])
#     else:
#         print("no one is here")

#     with lock:
#         existing_smm = shared_memory.SharedMemory(name=smm_name)
#         np_array = np.ndarray((1, 20, 17, 2), dtype=np.float64, buffer=existing_smm.buf)
#         np_array[:]=bodyarry
#         existing_smm.close()
        
        
#def SkelCoord(smm_name,lock):
def SkelCoord(smm_name,actions,zed_signal_attrs,lock,lock1,lock2):
    bodyarry=create_array(smm_name,lock)
    # Create a Camera object
    zed = sl.Camera()

    # Create a InitParameters object and set configuration parameters
    init_params = sl.InitParameters()
    init_params.camera_resolution = sl.RESOLUTION.HD720  # Use HD720 video mode
    init_params.depth_mode = sl.DEPTH_MODE.PERFORMANCE
    init_params.coordinate_units = sl.UNIT.METER
    init_params.sdk_verbose = True

    # Open the camera
    
    err = zed.open(init_params)
    if err != sl.ERROR_CODE.SUCCESS:
        exit(1)

    body_params = sl.BodyTrackingParameters()
    # Different model can be chosen, optimizing the runtime or the accuracy
    body_params.detection_model = sl.BODY_TRACKING_MODEL.HUMAN_BODY_FAST
    body_params.enable_tracking = True
    body_params.image_sync = True
    body_params.enable_segmentation = False
    # Optimize the person joints position, requires more computations
    body_params.enable_body_fitting = True

    camera_infos = zed.get_camera_information()
    if body_params.enable_tracking:
        positional_tracking_param = sl.PositionalTrackingParameters()
        # positional_tracking_param.set_as_static = True
        positional_tracking_param.set_floor_as_origin = True
        zed.enable_positional_tracking(positional_tracking_param)

    print("Body tracking: Loading Module...")

    err = zed.enable_body_tracking(body_params)
    if err != sl.ERROR_CODE.SUCCESS:
        print(repr(err))
        zed.close()
        exit(1)

    bodies = sl.Bodies()
    body_runtime_param = sl.BodyTrackingRuntimeParameters()
    # For outdoor scene or long range, the confidence should be lowered to avoid missing detections (~20-30)
    # For indoor scene or closer range, a higher confidence limits the risk of false positives and increase the precision (~50+)
    body_runtime_param.detection_confidence_threshold = 50

    x = []
    y = []
    z = []
    x1 = []
    y1 = []
    z1 = []
    t = []
    while zed.grab() == sl.ERROR_CODE.SUCCESS:
        # await asyncio.sleep(0.1)
        err = zed.retrieve_bodies(bodies, body_runtime_param)
        if bodies.is_new:
            body_array = bodies.body_list
            
            #print(str(len(body_array)) + " Person(s) detected\n")              ##############################################################
    
            if len(body_array) > 0:
                first_body = body_array[0]
   
                def calculate_velocity(x, y, z, t):

                    # Calculate the velocity based on the change in position over time
                    if len(x) < 2 or len(y) < 2 or len(z) < 2 or len(t) < 2:
                        return [0,0,0]
                    
                    delta_x = x[-1] - x[-2]
                    delta_y = y[-1] - y[-2]
                    delta_z = z[-1] - z[-2]
                    delta_t = t[-1] - t[-2]
                    
                    velocity_x = abs(delta_x / delta_t)
                    velocity_y = abs(delta_y / delta_t)
                    velocity_z = abs(delta_z / delta_t)
                    del(x[0])
                    del(y[0])
                    del(z[0])
                    return velocity_x, velocity_y, velocity_z
                


                
                # Read the live XYZ coordinates from the global variable
                x.append(first_body.keypoint[7][0])
                y.append(first_body.keypoint[7][1])
                z.append(first_body.keypoint[7][2])
                x1.append(first_body.keypoint[4][0])
                y1.append(first_body.keypoint[4][1])
                z1.append(first_body.keypoint[4][2])
                
                
                # Get the current time
                current_time = time.time()
                t.append(current_time)
                
                # Calculate the velocity
                l_Elbow = calculate_velocity(x, y, z, t)
                r_Wrist = calculate_velocity(x1, y1, z1, t)
                if len(t) == 2:
                    del(t[0])
                                #Global ZED Variables
                lock2.acquire()
                try:
                    zed_signal_attrs['confidence'] = first_body.confidence
                    zed_signal_attrs['id1'] = first_body.id
                    zed_signal_attrs['position'] = first_body.position
                    zed_signal_attrs['velocity'] = first_body.velocity
                    zed_signal_attrs['action_state'] = first_body.action_state
                    zed_signal_attrs['keypoint'] = first_body.keypoint
                    zed_signal_attrs['keypoint_2d'] = first_body.keypoint_2d
                    zed_signal_attrs['tracking_state'] = first_body.tracking_state
                    zed_signal_attrs['l_Elbow'] = l_Elbow
                    zed_signal_attrs['r_Wrist'] = r_Wrist
                    zed_signal_attrs['detected']= len(body_array)
                finally:
                    lock2.release()

                if first_body.confidence>80:
                       bodyarry= add_item(smm_name,lock,first_body.keypoint_2d,bodyarry )
            

            
            lock2.acquire()
            try:
                zed_signal_attrs['detected']= len(body_array)
            finally:
                    lock2.release()

    # Close the camera
    zed.close()
    
    
if __name__ == "__main__":
    SkelCoord()


