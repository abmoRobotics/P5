import math

from matplotlib.pyplot import plot
from path_planning.crack import Crack
from path_planning.frame import Frame
import cv2
import numpy as np
from path_planning.path_planning import find_path
import random

from vision import NpEncoder

HEIGHT = 480
WIDTH = 320
INCREMENT = 0.25 # 20% of 1m = 20cm 
PIXEL_INCREMENT = HEIGHT*INCREMENT

def test():
    a = []
    b = []
    c = []
    for i in range(0,130):
        a.append([math.floor(50+10*math.sin(i/20)),10+i*2])
    for i in range(0,170):
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

def plotPathPlanning():
    from path_planning.utils import map_cracks
    frame = test()
    frame0 = test0()
    frame.find_path()
    #find_path(frame)
    map_cracks(frame,frame0,480*0.75)
    #frame0 = find_path(frame0)
    frame0.find_path()
    frame0Vis = visualize(frame, frame.path,480*0.75)
    frame1Vis = visualize(frame0, frame0.path,480*0.25)

    # with open('output.txt', 'w') as f:
    #     for point in frame.path:
    #         f.write(str(point[0]))
    #         f.write(",")
    #         f.write(str(point[1]))
    #         f.write(",")
    #         f.write(str(point[2]))
    #         f.write('\n')

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

def convert_binary_image_to_json(input_file,json_output,path_output):
    from skimage.morphology import skeletonize
    from utils.features import process_image
    #from path_planning.frame import Frame
   # from path_planning.crack import Crack
    from path_planning.path_planning import (WIDTH, find_path)
    import json

    img = cv2.imread(f"test_data/Path_Planning_Json/{input_file}", cv2.IMREAD_GRAYSCALE)
    (thresh, blackAndWhiteImage) = cv2.threshold(img, 127, 1, cv2.THRESH_BINARY)

    frame1 = Frame()


    sorted_cracks = process_image(blackAndWhiteImage)

    for crack in sorted_cracks:
        frame1.add_crack(Crack(crack))

    
    #frame1.find_path()
    frame1.find_path()

    data_array = frame1.get_json_array()

    # Clear file
    open(f"test_data/Path_Planning_Json/{json_output}", 'w').close()

    for data in data_array:
        
        with open(f"test_data/Path_Planning_Json/{json_output}", 'a') as outfile:
            data = json.dumps(data,cls=NpEncoder)
            data = json.loads(data)
            json.dump(data, outfile)    
            outfile.write('\n')


    visual = visualize(frame1,frame1.path, 3200)
    cv2.imwrite(f"test_data/Path_Planning_Json/{path_output}",visual)


if __name__ == "__main__":
    # Take a binary image convert the image to a path in json format
    # convert_binary_image_to_json("crackAdvanced.png","json_advanced.txt","Advanced.png")
    # convert_binary_image_to_json("crackSimple.png","json_simple.txt","Simple.png")
    #convert_binary_image_to_json("test.png","sletmig.txt","path.png")
    plotPathPlanning()