import cv2
import numpy as np
from pathlib import Path
import os

left_dir_path = "left_mono_data"
right_dir_path = "right_mono_data"
dir_path = "stitch_data"
resize_dir_path = "resize_stitch_data"

Path(dir_path).mkdir(parents=True, exist_ok=True)
Path(resize_dir_path).mkdir(parents=True, exist_ok=True)

files = os.listdir(left_dir_path)
files.sort(key=lambda x:int(x[:-4]))#只适用于像一些“9.txt”、“6.jpg”等这类文件，而对于像"img_66.jpg"这种文件就完全没有用。此代码意思是倒数第四个数左边，例如“9.txt”、“6.jpg”，就只排序“9”、“6”
#files.sort(key=lambda x: int(x.split(".")[0].split("_")[1]))#对于像"img_66.jpg"这种文件，先对“.”分割，得到"img_66"，再对"_"分割，得到“66”.[0]代表保留分割后左边，[1]代表保留分割后右边
for file in files:
    print(file)

    img1 = cv2.imdecode(np.fromfile(f"{left_dir_path}/{file}", dtype=np.uint8), -1)
    img2 = cv2.imdecode(np.fromfile(f"{right_dir_path}/{file}", dtype=np.uint8), -1)
    # 纵向合并
    #img_zhong = np.vstack((img1, img2))
    # axis=1：横向合并 axis=0 纵向合并
    img_horizontal = np.concatenate([img1, img2], axis=1)
    #cv2.imshow('img_zhong', img_zhong)

    # cv2.namedWindow('img_horizontal', cv2.WINDOW_KEEPRATIO)
    # cv2.imshow('img_heng', img_horizontal)

    cv2.imwrite(f"{dir_path}/{file}", img_horizontal)

    img_horizontal = cv2.resize(img_horizontal, (1280, 720), interpolation=cv2.INTER_CUBIC)

    cv2.imwrite(f"{resize_dir_path}/{file}", img_horizontal)


