from annotator.formatter.utils.vis_yolo import vis_yolo

task = 'detection'
# task = 'segmentation'
input_dir = '/home/wonchul/Downloads/sungwoo_edge/yolo_{}_split_dataset'.format(task)
output_dir = '/home/wonchul/Downloads/sungwoo_edge/vis_yolo_{}'.format(task)
image_exts = ['bmp']

vis_yolo(task, input_dir, output_dir, image_exts)