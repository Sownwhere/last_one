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
        default=('configs/skeleton/posec3d/'
                 'slowonly_r50_8xb16-u48-240e_ntu60-xsub-keypoint.py'),
        help='skeleton model config file path')
    parser.add_argument(
        '--checkpoint',
        default=('checkpoint/'
                 'slowonly_r50_u48_240e_ntu60_xsub_keypoint-f3adabf1.pth'),
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


def visualize(args, frames, data_samples, action_label):
    pose_config = mmengine.Config.fromfile(args.pose_config)
    visualizer = VISUALIZERS.build(pose_config.visualizer)
    visualizer.set_dataset_meta(data_samples[0].dataset_meta)

    vis_frames = []
    print('Drawing skeleton for each frame')
    for d, f in track_iter_progress(list(zip(data_samples, frames))):
        f = mmcv.imconvert(f, 'bgr', 'rgb')
        visualizer.add_datasample(
            'result',
            f,
            data_sample=d,
            draw_gt=False,
            draw_heatmap=False,
            draw_bbox=True,
            show=False,
            wait_time=0,
            out_file=None,
            kpt_thr=0.3)
        vis_frame = visualizer.get_image()
        cv2.putText(vis_frame, action_label, (10, 30), FONTFACE, FONTSCALE,
                    FONTCOLOR, THICKNESS, LINETYPE)
        vis_frames.append(vis_frame)

    vid = mpy.ImageSequenceClip(vis_frames, fps=24)
    vid.write_videofile(args.out_filename, remove_temp=True)

import time 
def main():
    args = parse_args()

    # tmp_dir = tempfile.TemporaryDirectory()
    # frame_paths, frames = frame_extract(args.video, args.short_side,
    #                                     tmp_dir.name)
    # frame_paths = frame_paths[:52]  # 保留每隔一个元素的路径
    # frames = frames[:52]  # 保留每隔一个元素的帧图像
    # num_frame = len(frame_paths)
    # print("here is something",num_frame)

    # h, w, _ = frames[0].shape
    # print(h,w)
 
    # Get Human detection results.
    #print("start time .....")
    #s = time.time()
    # det_results, _ = detection_inference(args.det_config, args.det_checkpoint,
    #                                      frame_paths, args.det_score_thr,
    #                                      args.det_cat_id, args.device)
    # # 将det_results转换为NumPy数组
    # # det_results_np = np.array(det_results)

    # # # 将det_results_np转换为2D数组
    # # det_results_2d = det_results_np.reshape(det_results_np.shape[0], -1)

    # # # 保存目标检测结果到文本文件
    # # np.savetxt('det_results.txt', det_results_2d, fmt='%s')
    # torch.cuda.empty_cache()
    

    

    # # Get Pose estimation results.
    # pose_results, pose_data_samples = pose_inference(args.pose_config,
    #                                                  args.pose_checkpoint,
    #                                                  frame_paths, det_results,
    #                                                  args.device)


    # torch.cuda.empty_cache()
    #e = time.time()
    #print("running time is ",e-s)
    # h=720 
    # w = 1280
    h=400 
    w = 800
    
    num_frame =10
    fake_anno = dict(
        frame_dir='',
        label=-1,
        img_shape=(h, w),
        original_shape=(h, w),
        start_index=0,
        modality='Pose',
        total_frames=num_frame)
    # num_person = max([len(x['keypoints']) for x in pose_results])

    num_keypoint = 17
    # keypoint = np.zeros((num_frame, num_person, num_keypoint, 2),
    #                     dtype=np.float16)
    # keypoint_score = np.zeros((num_frame, num_person, num_keypoint),
    #                           dtype=np.float16)
    # for i, poses in enumerate(pose_results):
    #     keypoint[i] = poses['keypoints']
    #     keypoint_score[i] = poses['keypoint_scores']

    # print(keypoint.shape)
    
    # fake_anno['keypoint'] = keypoint.transpose((1, 0, 2, 3))
    # fake_anno['keypoint_score'] = keypoint_score.transpose((1, 0, 2))
    # print(fake_anno['keypoint'])
    # # print(len(fake_anno['keypoint']))
    # np.save('keypoint.npy', fake_anno.get('keypoint', np.array([])))
    # np.save('keypoint_score.npy', fake_anno.get('keypoint_score', np.array([])))

    print("star time")
    s = time.time()
    tmp = np.load('skeletonpose1.npy', allow_pickle=True)
    tmp = tmp[:,:10,:,:]
    fake_anno['keypoint'] =np.copy(tmp)
    print(fake_anno['keypoint'].shape)
    tmp1 = np.load('keypoint_score.npy', allow_pickle=True)
    tmp1 = tmp1[:,:10,:]
    fake_anno['keypoint_score'] = np.copy(tmp1)
    print(fake_anno['keypoint_score'].shape)
    e = time.time()
    print("the processing1 time is ",e-s)
    
    s = time.time()
    config = mmengine.Config.fromfile(args.config)
    config.merge_from_dict(args.cfg_options)
    e = time.time()
    print("the processing2 time is ",e-s)
    
    model = init_recognizer(config, args.checkpoint, args.device)
    print("star")
    for i in range(100):
        s = time.time()
        fake_anno = dict(
        frame_dir='',
        label=-1,
        img_shape=(h, w),
        original_shape=(h, w),
        start_index=0,
        modality='Pose',
        total_frames=num_frame)
        fake_anno['keypoint'] =np.copy(tmp)
        fake_anno['keypoint_score'] = np.copy(tmp1)
        result = inference_recognizer(model, fake_anno)
        max_pred_index = result.pred_scores.item.argmax().item()
        e = time.time()
    
        print("the processing3 time is ",e-s)
    label_map = [x.strip() for x in open(args.label_map).readlines()]
    action_label = label_map[max_pred_index]
    print("hhhhhhhhhhhhhhhhhhhhhhhhh",action_label)

    # visualize(args, frames, pose_data_samples, action_label)

    # ...


if __name__ == '__main__':
    main()
