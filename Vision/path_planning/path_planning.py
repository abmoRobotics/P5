
from frame import Frame
from crack import Crack
import cv2
import math
import random
import numpy as np

HEIGHT = 480
WIDTH = 320
INCREMENT = 0.25 # 20% of 1m = 20cm 
PIXEL_INCREMENT = HEIGHT*INCREMENT


def find_path(frame):
    # Path plan until next frame is ready
    while not frame._next_frame_ready() and not frame.cracks_done():
        # Get the object where the first crack begins
        max_pixel, obj_index = frame._largest_y_value()
        
        #while not frame.cracks[obj_index].is_done():
        for idx in range(
            frame.cracks[obj_index].get_index(), # Get the current crack not repaired
            frame.cracks[obj_index].len          # Run for loop until last object is reached
            ):
            max_pixel2, obj_index2 = frame._largest_y_value()
            # If next frame is ready exit for loop and continue with next frame
            if frame._next_frame_ready():
                break
            # Check if should shift to another crack
            elif (((frame.cracks[obj_index].get_current_crack()[1]) > (max_pixel2 + PIXEL_INCREMENT)) or (frame.cracks[obj_index]._is_done)):
                frame.cracks[obj_index].shift()
                frame.path.append(frame.cracks[obj_index].get_current_crack())
                #print("From", frame.cracks[obj_index].get_current_crack())
                frame.cracks[obj_index2].shift()
                #print("To", frame.cracks[obj_index2].get_current_crack())
                obj_index = obj_index2
                break
            # Point will be repaired
            else:
                frame.path.append(frame.cracks[obj_index].get_current_crack())
                frame.cracks[obj_index].repair()

    return frame

def test():
    a = []
    b = []
    c = []

    for i in range(0,170):
        a.append([math.floor(50+10*math.sin(i/20)),10+i*2])
        b.append([math.floor(170-20*math.exp(i/100)),170+i*2])
        c.append([math.floor(200+20*math.exp(i/100)),100+i*2])


    c1 = Crack(a)
    c2 = Crack(b)
    c3 = Crack(c)

    frame = Frame()
    frame.add_crack(c1)
    frame.add_crack(c2)
    frame.add_crack(c3)
    return frame

def test0():
    a = []
    b = []
    c = []
    d = []

    for i in range(0,170):
        if 10-360+i*2 > 0:
            a.append([math.floor(50+10*math.sin(i/20)),10-360+i*2])
        if 170-360+i*2 > 0:
            b.append([math.floor(170-20*math.exp(i/100)),170-360+i*2])
        if 100-360+i*2 > 0:
            c.append([math.floor(200+20*math.exp(i/100)),100-360+i*2])
        d.append([math.floor(170-20*math.exp(i/100)),170+i])

    frame = Frame()

    if a:
        c1 = Crack(a)
        frame.add_crack(c1)
    if b:
        c2 = Crack(b)
        frame.add_crack(c2)
    if c:
        c3 = Crack(c)
        frame.add_crack(c3)
    c4 = Crack(d)
    frame.add_crack(c4)
    return frame
def test2():
    a = []
    b = []
    c = []

    for i in range(0,150):
        a.append([50,10+i*2])
        b.append([170,170+i*2])
        c.append([200,100+i*2])


    c1 = Crack(a)
    c2 = Crack(b)
    c3 = Crack(c)

    frame = Frame()
    frame.add_crack(c1)
    frame.add_crack(c2)
    frame.add_crack(c3)
    return frame

def test3():
    a = []
    b = []

    for i in range(0,55):
        a.append([170,i*2])
    for i in range(0,20):
        b.append([200,i*2])


    c1 = Crack(a)
    c2 = Crack(b)

    frame = Frame()
    frame.add_crack(c1)
    frame.add_crack(c2)
    return frame
    

def visualize(frame: Frame, p1, offset):
    blank_image = np.zeros((HEIGHT,WIDTH,3), np.uint8)
    
    shifts = 0

    for crack in frame.cracks:
        cords = crack.get_coordinates()
        for i in range(0,len(cords)-1):
            x, y = cords[i][0], cords[i][1]
            x1, y1 = cords[i+1][0], cords[i+1][1]
            cv2.line(blank_image, (x, y), (x1, y1), (0, 0, 255), thickness=2, lineType=4)
            
    for i in range(0,len(p1)-1):
        x, y = p1[i][0], p1[i][1]
        x1, y1 = p1[i+1][0], p1[i+1][1]
       # print(p.path[i])
        n = i/255
        n = math.floor(n)
        if ((n%2) == 0):
            color = i%255
        else:
            color = 255 - (i%255)
        #print(p.path[i][2],p.path[i+1][2])
        if (p1[i][2] and p1[i+1][2]):
            shifts += 1
            cv2.line(blank_image, (x, y), (x1, y1), (random.randint(100,255), random.randint(0,25),random.randint(0,255)), thickness=1, lineType=8)
            center = [math.floor(x+((x1-x)/2)), math.floor(y + ((y1-y)/2))]
            cv2.putText(blank_image, str(shifts),(center[0],center[1]),cv2.FONT_HERSHEY_SIMPLEX,0.4,(0, 255, 0))
            #print("Shift")
        else:
            cv2.line(blank_image, (x, y), (x1, y1), (255, 255, 255), thickness=2, lineType=8)

        cv2.line(blank_image, (0, math.floor(offset)), (WIDTH, math.floor(offset)), (0, 255, 255), thickness=1, lineType=8)
        
    return blank_image







from utils import map_cracks
frame = test()
frame0 = test0()
find_path(frame)
map_cracks(frame,frame0,480*0.75)
frame0 = find_path(frame0)
frame0Vis = visualize(frame, frame.path,480*0.75)
frame1Vis = visualize(frame0, frame0.path,480*0.25)

while 1:
    cv2.imshow("frame",frame0Vis)
    cv2.imshow("frame2",frame1Vis)
    cv2.waitKey(20)




frame2 = test3()
frame1 = test2()
frame1 = find_path(frame1)
map_cracks(frame1,frame2,480*0.75)
frame2 = find_path(frame2)
frame1Vis = visualize(frame1, frame1.path,480*0.75)
frame2Vis = visualize(frame2, frame2.path,480*0.25)
while 1:
    cv2.imshow("frame",frame1Vis)
    cv2.imshow("frame2",frame2Vis)
    cv2.waitKey(20)

