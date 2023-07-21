
from imports import *
from Prerequisites import *
from Glob import Glob
import time

import winsound
freq=1000
dur=20

def coco18_translate_coco17(array):
    #delete the nose
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


#def SkelCoord():
def SkelCoord():
    
    #Declare Globals
    global confidence, ID, Velocity, AS, threedim, twodim, bowing
    
    # Create a Camera object
    zed = sl.Camera()

    # Create a InitParameters object and set configuration parameters
    init_params = sl.InitParameters()
    init_params.camera_resolution = sl.RESOLUTION.HD720  # Use HD720 video mode
    print(init_params.camera_resolution)
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
    t = []
    while zed.grab() == sl.ERROR_CODE.SUCCESS:

        err = zed.retrieve_bodies(bodies, body_runtime_param)
        if bodies.is_new:
            body_array = bodies.body_list
            Glob.detected= len(body_array)
            print(str(len(body_array)) + " Person(s) detected\n")
    
            if len(body_array) > 0:
                first_body = body_array[0]
                
                #Global ZED Variables
                Glob.confidence = first_body.confidence
                Glob.ID = first_body.id
                Glob.Position = first_body.position
                Glob.Velocity = first_body.velocity
                Glob.AS = first_body.action_state
                Glob.threedim = first_body.keypoint
                Glob.twodim = first_body.keypoint_2d
                Glob.trackingstate = first_body.tracking_state
                
                
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
                    del(t[0])
                    
                    
                    return velocity_x, velocity_y, velocity_z


                
                # Read the live XYZ coordinates from the global variable
                x.append(Glob.threedim[7][0])
                y.append(Glob.threedim[7][1])
                z.append(Glob.threedim[7][2])
                
                
                # Get the current time
                current_time = time.time()
                t.append(current_time)
                
                # Calculate the velocity
                Glob.l_Elbow = calculate_velocity(x, y, z, t)
                # signal_Wing()

    # Close the camera
    zed.close()
    
    
if __name__ == "__main__":
    SkelCoord()
