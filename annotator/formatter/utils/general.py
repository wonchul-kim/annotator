import os.path as osp 
from glob import glob 

def search_folders(input_dir, logger=None):
    
    folders = [folder.split("/")[-1] for folder in glob(osp.join(input_dir, "**")) if not osp.isfile(folder)]

    if len(folders) == 0:
        folders = ['./']

    if logger is not None:
        logger.info(f"There are {folders}")
    else:
        print(f"There are {folders}")

    return folders

def search_img_file(input_dir, folder, image_exts):
    return [file for ext in image_exts for file in glob(osp.join(input_dir, folder, f'*.{ext}'))]

