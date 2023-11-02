import os
import cv2
import numpy as np
from pathlib import Path

path = 'resize_stitch_data'
filelist = os.listdir(path)
filelist.sort(key=lambda x:int(x[:-4]))#只适用于像一些“9.txt”、“6.jpg”等这类文件，而对于像"img_66.jpg"这种文件就完全没有用。

dir_path = "stitch_video"
Path(dir_path).mkdir(parents=True, exist_ok=True)

fps = 24  # 视频每秒24帧
size = (1280, 720)  # 需要转为视频的图片的尺寸
# 可以使用cv2.resize()进行修改

video = cv2.VideoWriter(dir_path+"/"+"VideoTest2.mp4", cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), fps, size)
# 视频保存在当前目录下

for item in filelist:
    if item.endswith('.png'):
        # 找到路径中所有后缀名为.png的文件，可以更换为.jpg或其它
        item = path +'/' + item
        img = cv2.imread(item)
        print(item)
        video.write(img)

video.release()
cv2.destroyAllWindows()