import cv2 
import numpy as np
import imgviz
import os.path as osp 
import os
from utils import search_folders, search_img_file, xywh2xyxy

def read_labels_txt_file(txt_file):
    labels = []
    with open(txt_file, 'r') as f:
        while True:
            line = f.readline().strip('\n')
            if not line: break 

            labels.append(str(line))

    return labels

def read_yolo_text_file(txt_file):
    anns = []
    with open(txt_file, 'r') as f:
        
        while True:
            line = f.readline().strip('\n')
            if not line: break 
            
            line = line.split(" ")
            
            anns.append([int(line[0])] + list(map(float, line[1:])))   

    return anns

def vis_seg_img(img, anns, labels, width, height, color_map):
    for ann in anns:
        polygon = []
        xs, ys = [], []
        label = int(ann[0])
        for idx, val in enumerate(ann[1:]):
            if idx%2 == 0:
                xs.append(val*width)
            else:
                ys.append(val*height)
                polygon.append([xs[-1], ys[-1]])

        color = [int(c) for c in color_map[label + 1]]
        cv2.putText(img, labels[label], (int(np.min(xs)), int(np.min(ys)) - 5), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, tuple(color), 1)
        cv2.rectangle(img, (int(np.min(xs)), int(np.min(ys))),
                                (int(np.max(xs)), int(np.max(ys))),
                    tuple(color), 1)
        cv2.fillPoly(img, [np.array(polygon, dtype=np.int32)], tuple(color))

def vis_det_img(img, anns, labels, width, height, color_map):
    for ann in anns:
        label = int(ann[0])
        assert len(ann[1:]) == 4, RuntimeError(f"The length of points for xywh must be 4, not {len(ann[1:])} as {ann[1:]}")
        print(ann[1:])
        xyxy = xywh2xyxy((height, width), ann[1:])
        print(xyxy, width, height)

        color = [int(c) for c in color_map[label + 1]]
        cv2.putText(img, labels[label], (int(xyxy[0]), int(xyxy[1]) - 5), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, tuple(color), 1)
        cv2.rectangle(img, (int(xyxy[0]), int(xyxy[1])),
                                (int(xyxy[2]), int(xyxy[3])),
                    tuple(color), 1)

def vis_yolo_seg(input_dir, output_dir, image_exts):

    if not osp.exists(output_dir):
        os.makedirs(output_dir)

    color_map = imgviz.label_colormap()
    
    folders = search_folders(input_dir)
    labels = read_labels_txt_file(osp.join(input_dir, 'classes.txt'))
    for folder in folders:
        _output_dir = osp.join(output_dir, folder)
        if not osp.exists(_output_dir):
            os.mkdir(_output_dir)

        img_files = search_img_file(input_dir, folder, image_exts)

        for img_file in img_files:
            img = cv2.imread(img_file)
            (height, width, channel) = img.shape
            filename = osp.split(osp.splitext(img_file)[0])[-1]
            txt_file = osp.splitext(img_file)[0] + '.txt'

            assert osp.exists(txt_file), FileNotFoundError(f"There is no such json-file: {txt_file}")

            anns = read_yolo_text_file(txt_file)
            if task == 'segmentation':
                vis_seg_img(img, anns, labels, width, height, color_map)
            elif task == 'detection':
                vis_det_img(img, anns, labels, width, height, color_map)
            cv2.imwrite(osp.join(_output_dir, f'{filename}.bmp'), img)                
                
                
task = 'detection'
# task = 'segmentation'
input_dir = '/home/wonchul/Downloads/sungwoo_edge/yolo_{}_split_dataset'.format(task)
output_dir = '/home/wonchul/Downloads/sungwoo_edge/vis_yolo_{}'.format(task)
image_exts = ['bmp']

vis_yolo_seg(input_dir, output_dir, image_exts)