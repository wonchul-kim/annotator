import os
import os.path as osp
from shutil import copyfile
import json
import numpy as np
from utils import search_folders, search_img_file, xyxy2xywh


def is_ignore_case(ann):
    if ann['shape_type'].lower() == 'point':
        return True 
    elif ann['shape_type'].lower() in ['polygon', 'watershed']:
        if len(ann['points']) < 3:
            return True 
        else:
            return False 
    elif ann['shape_type'] == 'circle':
        NotImplementedError
    elif ann['shape_type'] == 'rectangle':
        assert len(ann['points']) == 2
        return False

def write_yolo_txt_file(output_dir, json_file, labels, task):
    with open(json_file, 'r') as f:
        anns = json.load(f)

    width = anns['imageWidth']
    height = anns['imageHeight']

    txt_file = open(osp.join(output_dir, 
                        osp.split(osp.splitext(json_file)[0])[-1] + '.txt'), 'w')
    for ann in anns['shapes']:
        label = ann['label']
        labels.add(label)
        points = ann['points']

        if is_ignore_case(ann):
            continue

        xs, ys = [], []
        data = str(list(labels).index(label))
        for xy in points:
            x, y = xy
            xs.append(x)
            ys.append(y)
            
            if task == 'segmentation':
                data += f" {x/width} {y/height}"

        if task == 'detection':
            for val in xyxy2xywh((height, width), [np.min(xs), np.min(ys), np.max(xs), np.max(ys)]):
                data += f" {val}"

        txt_file.write(data)
        txt_file.write("\n")
    txt_file.close()

def write_labels_txt_file(output_dir, labels):
    labels_txt_file = open(osp.join(output_dir, 'classes.txt'), 'w')
    for label in labels:
        labels_txt_file.write(label)
        labels_txt_file.write('\n')
    labels_txt_file.close()

def labelme_to_yolo(task, input_dir, output_dir, image_exts, copy_image=True,logger=None):

    if not osp.exists(output_dir):
        os.makedirs(output_dir)
    
    folders = search_folders(input_dir)
    labels = set()

    for folder in folders:
        
        _output_dir = osp.join(output_dir, folder)
        if not osp.exists(_output_dir):
            os.mkdir(_output_dir)

        img_files = search_img_file(input_dir, folder, image_exts)

        for img_file in img_files:
            filename = osp.split(osp.splitext(img_file)[0])[-1]
            json_file = osp.splitext(img_file)[0] + '.json'

            assert osp.exists(json_file), FileNotFoundError(f"There is no such json-file: {json_file}")

            write_yolo_txt_file(_output_dir, json_file, labels, task)

            if copy_image:
                copyfile(img_file, osp.join(_output_dir, filename + '.bmp'))

    write_labels_txt_file(output_dir, labels)
        
task = 'detection'
# task = 'segmentation'
input_dir = '/home/wonchul/Downloads/sungwoo_edge/split_dataset'
output_dir = '/home/wonchul/Downloads/sungwoo_edge/yolo_{}_split_dataset'.format(task)
image_exts = ['bmp']

labelme_to_yolo(task, input_dir, output_dir, image_exts)