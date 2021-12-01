from utils.features import (process_image,closing)
from PIL import Image
import numpy as np
from path_planning.crack import Crack
from path_planning.frame import Frame
from path_planning.path_planning import find_path
from path_planning.tests import (visualize)
import time
import cv2
img = Image.open(r"C:\P5\P5\Vision\data\train_masks\20160328_151013_361_1281.png").convert('L')
#img = Image.open(r"C:\P5\P5\Vision\data\train_masks\20160222_081102_1921_1.png").convert('L') 
img = np.array(img)
(thresh, blackAndWhiteImage) = cv2.threshold(img, 127, 1, cv2.THRESH_BINARY)
binary_image = closing(blackAndWhiteImage)
t1 = time.time()
sorted_cracks = process_image(binary_image)

frame1 = Frame()

for crack in sorted_cracks:
    frame1.add_crack(Crack(crack))


find_path(frame1) # 5 ms
print(time.time()-t1)
frame0Vis = visualize(frame1, frame1.path,640*1)

while 1:
    cv2.imshow("frame",frame0Vis)
    cv2.waitKey(20) 