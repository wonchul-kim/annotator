from annotator.formatter import labelme_to_yolo

task = 'detection'
# task = 'segmentation'
input_dir = '/home/wonchul/Downloads/sungwoo_edge/split_dataset'
output_dir = '/home/wonchul/Downloads/sungwoo_edge/yolo_{}_split_dataset'.format(task)
image_exts = ['bmp']

labelme_to_yolo(task, input_dir, output_dir, image_exts)