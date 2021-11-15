from utils.features import (skeletonization_with_threshold,
                            find_branches,
                            region_array,
                            sort_branch,
                            closing)
from PIL import Image
import numpy as np

from path_planning.crack import Crack
from path_planning.frame import Frame
from path_planning.path_planning import (find_path, visualize)
import time
import cv2
img = Image.open(r"C:\P5\P5\Vision\data\train_masks\20160328_151013_361_1281.png").convert('L')
#img = Image.open(r"C:\P5\P5\Vision\data\train_masks\20160222_081102_1921_1.png").convert('L') 
img = np.array(img)
img = closing(img)

t1 = time.time()
# Get skeleton
skeleton = skeletonization_with_threshold(img)

# Extract array with pixels from skeleton
skeleton_points = np.where(skeleton[:]==1)

# Convert to (x, y)
skeleton_points = list(zip(skeleton_points[1], skeleton_points[0]))

# Find branches
skeleton_branches = find_branches(skeleton, skeleton_points)

# Find regions
regions = region_array(skeleton_branches)
t2 = time.time()
# Sort regions WAITING FOR JESPER
sorted_cracks = sort_branch(regions)
t3 = time.time()
frame1 = Frame()

for c in sorted_cracks:
    l = []
    for o in c:
        l.append(list(o))

    a = Crack(l)
    frame1.add_crack(a)

for idx, a in enumerate(frame1.cracks):
    print(idx)

find_path(frame1)
t4 = time.time()
print(t2-t1)
print(t3-t1)
print(t4-t1)
frame0Vis = visualize(frame1, frame1.path,640*0.75)

while 1:
    cv2.imshow("frame",frame0Vis)
    cv2.waitKey(20)