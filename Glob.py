## G L O B A L    V A R I A B L E S ##

# UNIVERSAL ================================================================================

class Glob: 

    global_list = []

    robot_pos = [-0.1424, -0.2634,  2.6044]         # position of robot in relation to camera. X (L/R), Y (Up/Down). Measured in m
  
    camera_pos = [0,2,0]            # position of camera. X (L/R), Y (Up/Down), Z (Depth). Measured in m from back of L camera

    current_state = None            # current state
    current_behaviour = None        # active behaviour

    start_time = None               # start time of current behaviour
    t = None                        # elapsed time of current behaviour
    duration = None                 # duration of current behaviour

    p = [0,0,0]                     # chamber pressure array
    l0 = [0,0,0]                    # RGB top
    l1 = [0,0,0]                    # RGB bottom

    frame = [p, l0, l1]             # snapshot of vine at any moment 

    # Transitions

    # Bloop

    bloop_starting_0 = [0,0,0]
    bloop_starting_1 = [0,0,0]
    bloop_target_0 = [0,0,0]
    bloop_target_1 = [0,0,0]
    bloop_diff_0 = [0,0,0]
    bloop_diff_1 = [0,0,0]
    bloop_start_t = 0.0
    bloop_t = 0.0             # elapsed time

    # Shift

    shift_starting_p = [0,0,0]
    shift_target = [0,0,0]
    shift_diff = [0,0,0]
    shift_start_t = 0.0
    shift_t = 0.0

    # SkelCoord --------------------------------------------------------------------------------

    person1 = [0, 0, 0]             # xyz of person 1
    sextant = 0
    finalstate = 0                  # confident state from decision()
         
    # New Global ZED Variables
    confidence = None
    ID = None
    Position = []
    Velocity = None
    AS = None
    threedim = None
    twodim = None
    detected = 0    #######################################################################################################
    trackingstate =[]
    
    # Signals from gestures
    signBowing = False

    signclap = False
    repeat = 0
    signJump = False
    signWaving = False
    l_Elbow  =[0,0,0]
    r_Wrist = [0,0,0]
    signhug = False
    signtickle = False
    
    distance = 1000
    

    # STATE/BEHAVIOUR SPECIFIC =======================================================================

    # sleepin 

    breath_time = None 
    hold_time = None                         
    pause_time = None

    dream_breath = 0                    
    dream_breath_order = [1,2,3]

    dream_in = 0            # look to remove
    dream_out = 0

    # dreaming 

    dream_on = 1             # AAAAAAAAAAAA sing with me! sing for the years!           ##############################################
    dream_type =  0

    dA_0 = [0,0,0]
    dA_1 = [0,0,0]
    dB_0 = [0,0,0]
    dB_1 = [0,0,0]
    dC_0 = [0,0,0]
    dC_1 = [0,0,0]

    # wake 
    awake_start_colour = [[0,0,0],[0,0,0]]
    wait_threshold = 0
    action_duration = 0

    neutral_colour = [[0,0,0],[0,0,0]]

    # neutral
    neutral_1 = [0,0,0]
    
    # hug type
    hug_type = 0
    #action label
    actions=None