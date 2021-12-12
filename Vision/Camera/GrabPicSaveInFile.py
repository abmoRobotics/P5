import cv2
from vimba import *
import numpy as np
import time

VELOCTY = 2.22 # 2.22m/s = 8km/h
WORKSPACEHEIGHT =  1.6 # Ved ikke om dette er korrekt?
OVERLAP_PERCENTAGE = 0.25 

delay = (WORKSPACEHEIGHT*(1-OVERLAP_PERCENTAGE))/VELOCTY
i = 0
fourcc = cv2.VideoWriter_fourcc('X','V','I','D')

videoWriter = cv2.VideoWriter('C:/Users/N/Desktop/video.avi', fourcc, 30.0, (2560,480))

frame = np.zeros((1000, 1000))
with Vimba.get_instance() as vimba:
    cams = vimba.get_all_cameras()
    start_time = time.time()
    with cams[0] as cam:
        while(1):
            if (time.time()-start_time > start_time+delay):
                frame = cam.get_frame()
                start_time = time.time()
                frame.convert_pixel_format(PixelFormat.Bgr8)
                videoWriter.write(frame)