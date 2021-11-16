import cv2
from vimba import *
import numpy as np
import time
cv2.namedWindow("Picture")
frame = np.zeros((1000, 1000))
with Vimba.get_instance() as vimba:
    cams = vimba.get_all_cameras()
    with cams[0] as cam:
        while(1):
            timestart = time.time()
            frame = cam.get_frame()
            frame.convert_pixel_format(PixelFormat.Bgr8)
            cv2.imshow("Picture", frame.as_opencv_image())
            cv2.waitKey(10)
            timestop = time.time()
            print("Took ", timestop - timestart, " seconds with ", 1/(timestop-timestart), " FPS")