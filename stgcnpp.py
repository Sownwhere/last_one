# Copyright (c) OpenMMLab. All rights reserved.
import argparse
import tempfile

import cv2
import mmcv
import mmengine
import numpy as np
import torch
from mmengine import DictAction
from mmengine.utils import track_iter_progress

from mmaction.apis import (detection_inference, inference_recognizer,
                           init_recognizer, pose_inference)
from mmaction.registry import VISUALIZERS
from mmaction.utils import frame_extract

try:
    import moviepy.editor as mpy
except ImportError:
    raise ImportError('Please install moviepy to enable output file')

FONTFACE = cv2.FONT_HERSHEY_DUPLEX
FONTSCALE = 0.75
FONTCOLOR = (255, 255, 255)  # BGR, white
THICKNESS = 1
LINETYPE = 1


def parse_args():
    parser = argparse.ArgumentParser(description='MMAction2 demo')
    # parser.add_argument('video', help='video file/url')
    # parser.add_argument('out_filename', help='output filename')
    parser.add_argument(
        '--config',
        default=('configs/skeleton/stgcnpp/'
                 'stgcnpp_8xb16-joint-u100-80e_ntu60-xsub-keypoint-2d.py'),
        help='skeleton model config file path')
    parser.add_argument(
        '--checkpoint',
        default=('checkpoint/'
                 'stgcnpp_8xb16-joint-u100-80e_ntu60-xsub-keypoint-2d_20221228-86e1e77a.pth'),
        help='skeleton model checkpoint file/url')
    parser.add_argument(
        '--det-config',
        default='configs1/faster-rcnn_r50_fpn_2x_coco_infer.py',
        help='human detection config file path (from mmdet)')
    parser.add_argument(
        '--det-checkpoint',
        default=('http://download.openmmlab.com/mmdetection/v2.0/faster_rcnn/'
                 'faster_rcnn_r50_fpn_2x_coco/'
                 'faster_rcnn_r50_fpn_2x_coco_'
                 'bbox_mAP-0.384_20200504_210434-a5d8aa15.pth'),
        help='human detection checkpoint file/url')
    parser.add_argument(
        '--det-score-thr',
        type=float,
        default=0.9,
        help='the threshold of human detection score')
    parser.add_argument(
        '--det-cat-id',
        type=int,
        default=0,
        help='the category id for human detection')
    parser.add_argument(
        '--pose-config',
        default='configs1/'
        'td-hm_hrnet-w32_8xb64-210e_coco-256x192_infer.py',
        help='human pose estimation config file path (from mmpose)')
    parser.add_argument(
        '--pose-checkpoint',
        default=('https://download.openmmlab.com/mmpose/top_down/hrnet/'
                 'hrnet_w32_coco_256x192-c78dce93_20200708.pth'),
        help='human pose estimation checkpoint file/url')
    parser.add_argument(
        '--label-map',
        default='datalable/label_map_ntu60.txt',
        help='label map file')
    parser.add_argument(
        '--device', type=str, default='cuda:0', help='CPU/CUDA device option')
    parser.add_argument(
        '--short-side',
        type=int,
        default=480,
        help='specify the short-side length of the image')
    parser.add_argument(
        '--cfg-options',
        nargs='+',
        action=DictAction,
        default={},
        help='override some settings in the used config, the key-value pair '
        'in xxx=yyy format will be merged into config file. For example, '
        "'--cfg-options model.backbone.depth=18 model.backbone.with_cp=True'")
    args = parser.parse_args()
    return args

import time 
def main(smm_name,actions,zed_signal_attrs,lock,lock1,lock2):
    from multiprocessing import shared_memory

    args =parse_args()
    h=720 
    w = 1280
    num_frame =20
    keypoint = 17
    fake_anno = dict(
        frame_dir='',
        label=-1,
        img_shape=(h, w),
        original_shape=(h, w),
        start_index=0,
        modality='Pose',
        total_frames=num_frame)

    print("star time")
    s = time.time()
    tmp = np.load('C:/Users/Science Gallery/Desktop/action_recognition/skeletondata/keypoint1.npy', allow_pickle=True)
    tmp = tmp[:,:20,:,:]
    fake_anno['keypoint'] =np.copy(tmp)
    print(fake_anno['keypoint'].shape)
    tmp1 = np.load('C:/Users/Science Gallery/Desktop/action_recognition/skeletondata/keypoint_score1.npy', allow_pickle=True)
    tmp1 = tmp1[:,:20,:]
    fake_anno['keypoint_score'] = np.copy(tmp1)
    print(fake_anno['keypoint_score'].shape)
    e = time.time()
    # print("the processing1 time is ",e-s)

    config = mmengine.Config.fromfile(args.config)
    config.merge_from_dict(args.cfg_options)
    model = init_recognizer(config, args.checkpoint, args.device)
    
    print("star")
    while True:
        s = time.time() 
        with lock:
            existing_smm = shared_memory.SharedMemory(name=smm_name)
            np_array = np.ndarray((1, num_frame,  keypoint, 2), dtype=np.float64, buffer=existing_smm.buf)
            tmp[:]=np_array
            existing_smm.close()

        fake_anno['keypoint'] =tmp
        fake_anno['keypoint_score'] = np.copy(tmp1)
        result = inference_recognizer(model, fake_anno)
        max_pred_index = result.pred_scores.item.argmax().item()
        e = time.time()
        label_map = [x.strip() for x in open(args.label_map).readlines()]
        action_label = label_map[max_pred_index]
        with lock1:
            if len(actions) >= 1:  # 如果共享列表的长度已经达到4
                del actions[0] 
            actions.append(action_label)
        
        
        # print("the processing3 time is ",e-s)
        # with lock2:
        #     if zed_signal_attrs['confidence'] is not None:
        #         print(zed_signal_attrs['confidence'])
        #     else:
        #         print("few")
    with lock:
        existing_smm = shared_memory.SharedMemory(name=smm_name)
        np_array = np.ndarray((1, num_frame, keypoint, 2), dtype=np.float64, buffer=existing_smm.buf)
        print(np_array)  
        existing_smm.close()
        
        
        



if __name__ == '__main__':
    import skelCoord
    from multiprocessing import shared_memory, Process, Lock, Manager
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
            'r_Wrist': [0,0,0]
        })
        
        lock = Lock()  #for the skeleton date
        lock1 = Lock() #for the action label
        lock2=  Lock() #for the zed_signal

        # pass zed_signal_attrs as an argument
        p1 = Process(target=skelCoord.SkelCoord, args=(smm.name, actions, zed_signal_attrs, lock, lock1, lock2))
        p2 = Process(target=main, args=(smm.name, actions, zed_signal_attrs, lock, lock1, lock2))
        
        p1.start()
        p2.start()

        p1.join()
        p2.join()

        smm.close()
        smm.unlink()
