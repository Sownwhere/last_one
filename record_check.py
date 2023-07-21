########################################################################
#
# Copyright (c) 2022, STEREOLABS.
#
# All rights reserved.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
########################################################################

"""
    Read SVO sample to read the video and the information of the camera. It can pick a frame of the svo and save it as
    a JPEG or PNG file. Depth map and Point Cloud can also be saved into files.
"""

import sys
import pyzed.sl as sl
import cv2
import numpy as np
from multiprocessing import shared_memory

class action__recognition():
    frame_num = 52
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
            np_array = np.ndarray((1, 52, 17, 2), dtype=np.float64, buffer=existing_smm.buf)
            np_array[:]=bodyarry
            existing_smm.close()
    return bodyarry
    
    
def write_date(smm_name,lock,bodyarry):
    with lock:
        existing_smm = shared_memory.SharedMemory(name=smm_name)
        np_array = np.ndarray((1, 52, 17, 2), dtype=np.float64, buffer=existing_smm.buf)
        np_array[:]=bodyarry
        existing_smm.close()
def coco18_translate_coco17(array):
    #delete the neck
    new_array = np.copy(array)
    new_array = np.delete(new_array, 1, axis=0)   
      
    new_array[0]=array[0]  # nose
    new_array[1]=array[14] # left_eye
    new_array[2]=array[13]  #right_eye
    new_array[3]=array[16]  #left_ear
    new_array[4]=array[15]  #right_ear
    new_array[5]=array[4]   #left_shoulder
    new_array[6]=array[1]   #right_shoulder
    new_array[7]=array[5]   #left_elbow
    new_array[8]=array[2]   #right_elbow
    new_array[9]=array[6]   #left_wrist
    new_array[10]=array[3]  #right_wrist
    new_array[11]=array[10] # left_hip
    new_array[12]=array[7]  # right_hip
    new_array[13]=array[11] #left_knee
    new_array[14]=array[8]  # right_knee
    new_array[15]=array[12] #left_ankle
    new_array[16]=array[9]  #right_ankle
    return new_array

def add_item(smm_name,lock,twodim,bodyarry):
    tmp = coco18_translate_coco17(twodim)
    # print(len(tmp))              

    if action__recognition.count >=action__recognition.frame_num:
        print("well")
        bodyarry= bodyarry[1:]
        action__recognition.count = 52
        bodyarry =np.concatenate((bodyarry, [tmp]), axis=0)
        #store the bodyarry into smm
        write_date(smm_name,lock,bodyarry)
    else:
        bodyarry[action__recognition.count]= np.copy(tmp)
        action__recognition.count = 1 +action__recognition.count
        print( action__recognition.count)
        write_date(smm_name,lock,bodyarry)
    return bodyarry

def delete_item(smm_name, count,bodyarry,lock): 
    count = count -1   
    if count>=0:
        tmp = 51 -count
        bodyarry[0][tmp][:] =  action__recognition.zeros_array
        print(bodyarry[0][tmp][:])
        
    else:
        print("no one is here")

    with lock:
        existing_smm = shared_memory.SharedMemory(name=smm_name)
        np_array = np.ndarray((1, 50, 17, 2), dtype=np.float64, buffer=existing_smm.buf)
        np_array[:]=bodyarry
        existing_smm.close()





def main(smm_name,lock):
    bodyarry = create_array(smm_name,lock)
        
    filepath = 'handwaving.svo'


    
    print("Reading SVO file: {0}".format(filepath))

    input_type = sl.InputType()
    input_type.set_from_svo_file(filepath)
    init = sl.InitParameters(input_t=input_type, svo_real_time_mode=False)

    cam = sl.Camera()
    status = cam.open(init)
    if status != sl.ERROR_CODE.SUCCESS:
        print(repr(status))
        exit()

    
    body_params = sl.BodyTrackingParameters()
    # Different model can be chosen, optimizing the runtime or the accuracy
    body_params.detection_model = sl.BODY_TRACKING_MODEL.HUMAN_BODY_FAST
    body_params.enable_tracking = True
    body_params.image_sync = True
    body_params.enable_segmentation = False
    # Optimize the person joints position, requires more computations
    body_params.enable_body_fitting = True

    camera_infos = cam.get_camera_information()
    if body_params.enable_tracking:
        positional_tracking_param = sl.PositionalTrackingParameters()
        # positional_tracking_param.set_as_static = True
        positional_tracking_param.set_floor_as_origin = True
        cam.enable_positional_tracking(positional_tracking_param)

    print("Body tracking: Loading Module...")
    err = cam.enable_body_tracking(body_params)
    if err != sl.ERROR_CODE.SUCCESS:
        print(repr(err))
        cam.close()
        exit(1)

    bodies = sl.Bodies()
    body_runtime_param = sl.BodyTrackingRuntimeParameters()
    # For outdoor scene or long range, the confidence should be lowered to avoid missing detections (~20-30)
    # For indoor scene or closer range, a higher confidence limits the risk of false positives and increase the precision (~50+)
    body_runtime_param.detection_confidence_threshold = 52
    
    
    runtime = sl.RuntimeParameters()
    mat = sl.Mat()
    bodies = sl.Bodies()
    obj_runtime_param = sl.ObjectDetectionRuntimeParameters()
    obj_runtime_param.detection_confidence_threshold = 40

    objects = sl.Objects()

    key = ''
    print("  Save the current image:     s")
    print("  Quit the video reading:     q\n")
    
    while key != 113:  # for 'q' key
        err = cam.grab(runtime)    
        # if err == sl.ERROR_CODE.SUCCESS:
        if cam.grab() == sl.ERROR_CODE.SUCCESS:
        #await asyncio.sleep(0.1)
            err = cam.retrieve_bodies(bodies, body_runtime_param)
            if bodies.is_new:
                body_array = bodies.body_list
                detected= len(body_array)
                # print(str(len(body_array)) + " Person(s) detected\n")
        
                if len(body_array) > 0:
                    first_body = body_array[0]
                    
                    #Global ZED Variables
                    confidence = first_body.confidence
                    ID = first_body.id
                    Position = first_body.position
                    Velocity = first_body.velocity
                    AS = first_body.action_state
                    threedim = first_body.keypoint
                    twodim = first_body.keypoint_2d
                    trackingstate = first_body.tracking_state
                
                    if confidence>80:
                       bodyarry= add_item(smm_name,lock,twodim,bodyarry )
            # else:
            #     delete_item(smm_name,action__recognition.count,bodyarry)
                    
            cam.retrieve_image(mat)

            key = cv2.waitKey(1)

        else:
            key = cv2.waitKey(1)
    cv2.destroyAllWindows()

    cam.close()
    print("\nFINISH")


if __name__ == "__main__":
    main()
