import logging
from multiprocessing import Thread, Lock, Event
import time
import numpy as np
import cv2
import copy
import torchvision
from torchvision import transforms
import albumentations as A
import numpy as np
import concurrent.futures
from vimba import *
from utils.utils import load_model
from albumentations.pytorch import ToTensorV2
import torch
from utils.features import process_image
from imageAligner import imageAlignerCPU, imageAlignerGPU
from path_planning import frame
from utils.features import process_image
from path_planning.frame import Frame
from path_planning.crack import Crack
from path_planning.path_planning import (WIDTH, find_path)
from path_planning.tests import visualize
from path_planning.utils import map_cracks

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
# Load the trained model
model = load_model("model/crack500BrightnessAugmentation.pth.tar")

# Parameters
HEIGHT = 320
WIDTH = 480
SIZE = WIDTH, HEIGHT,3

#Transforms
detect_transform = A.Compose(
        [
            A.Resize(height=HEIGHT, width=WIDTH),
            A.Normalize(
                mean=[0.0, 0.0, 0.0],
                std=[1.0, 1.0, 1.0],
                max_pixel_value=255.0,
            ),
            ToTensorV2(),
        ],
    )


# Locks
img_raw_lock = Lock()
img_seg_lock = Lock()
path_lock = Lock()

# Events
img_raw_event = Event()    
img_seg_event = Event()
transmit_event = Event()

# Global variables
img_raw = np.zeros(SIZE, dtype=np.uint8)
img_seg = np.zeros(SIZE, dtype=np.uint8)
path_transmit = []



def thread_get_image_test():
    print("Thread 1: Starting")
    global img_raw
    cap = cv2.VideoCapture(1)
    # try to get first frame
    if cap.isOpened():
        rval, frame = cap.read()
    else: 
        rval = False
    while rval:
        start_time = time.time()
        rval, frame = cap.read()

        with img_raw_lock:
            img_raw = frame
            img_raw_event.set()
        time.sleep(0.5)

def thread_get_image():
    print("Thread 1: Starting")
    global img_raw
    with Vimba.get_instance() as vimba:
        with vimba.get_camera_by_id("50-0536877557") as cam:
            while(1):
                time1 = time.time()
                # Get frame from camera
                time1 = time.time()
                frame = cam.get_frame()
                frame.convert_pixel_format(PixelFormat.Bgr8)
                frame = frame.as_numpy_ndarray()
                #print("FPS: %s", 1/(time.time()-time1))
                
                with img_raw_lock:
                    img_raw = frame
                    img_raw_event.set()
                print("FPS: %s", 1/(time.time()-time1))
                
def thread_run_model():
    print("Thread 2: Starting")
    global img_raw
    img_raw_old = np.zeros(([2, 2]), dtype=np.uint8)
    local_image = 0
    global img_seg
    while(1):
        img_raw_event.wait()
        img_raw_event.clear()
        with img_raw_lock:
            local_image = img_raw
            
            
        
        #print("IMGRAW", img_raw_old)
        # Find overlap

        
        if img_raw_old.any():
            t1 = time.time()
            new_image = cv2.cvtColor(local_image,cv2.COLOR_BGR2GRAY)
            new_image = cv2.resize(new_image,(WIDTH,HEIGHT),interpolation=cv2.INTER_AREA)
            t1 = time.time()
            traveled, overlapHeight = imageAlignerCPU(img_raw_old, new_image)
            print("TRAVELED: ", traveled, " TIME: ", time.time()-t1)

        #print(img_raw)
        augmentented = detect_transform(image=local_image)
        data = augmentented["image"].to(device=DEVICE)
        data = torch.unsqueeze(data,0)
        output = torch.sigmoid(model(data))
        output = torch.squeeze(output)
        preds = (output > 0.5).float()
        #cv2.imshow("preview", preds.cpu().numpy())
        # #cv2.imshow("normal", frame)
        #cv2.waitKey(1)
        
        img_raw_old = np.copy(local_image)
        img_raw_old = cv2.cvtColor(img_raw_old,cv2.COLOR_BGR2GRAY)
        img_raw_old = cv2.resize(img_raw_old,(480,320),interpolation=cv2.INTER_AREA)
        # Set data if lock is free 
        with img_seg_lock:
            img_seg = preds.cpu().numpy()
            img_seg_event.set()

    

def thread_path_plan():
    print("Thread 3: Starting")
    global img_seg
    global path_transmit
    img_old_seg = np.zeros(([2, 2]), dtype=np.uint8)
    old_frame = 0
    traveled = 0

    while True:
        img_seg_event.wait()    # Wait for new image
        img_seg_event.clear()   # Clear event
        
        # Get data if lock is free
        with img_seg_lock:
            local_img = img_seg.astype(np.uint8)
        t1 = time.time()
        
        #print(local_img.dtype)
        #(thresh, blackAndWhiteImage) = cv2.threshold(local_img, 127, 1, cv2.THRESH_BINARY)
        sorted_cracks = process_image(local_img)
        # if img_old_seg.any():
        #     #print("hej")
        #     traveled, overlapHeight = imageAlignerCPU(img_old_seg, local_img)
        #     #print("overlap", overlapHeight)
        img_old_seg = local_img
        frame1 = Frame()    
        
        

        for crack in sorted_cracks:
            frame1.add_crack(Crack(crack))
        
        
        if not old_frame == 0:
            #print("hej")
            #print(old_frame.path)
            map_cracks(old_frame,frame1,320*0.75)
        path1 = find_path(frame1)
       
        old_frame = copy.copy(frame1)
        # from path_planning.utils import map_cracks
        # if not old_frame == 0:
        #     map_cracks()
        
        
        # Set data if lock is free
        with path_lock:
            path_transmit = find_path(frame1)
            transmit_event.set()    # Set event true
        #print("FPS: ", 1/(time.time()-t1))
        frame0Vis = visualize(frame1, frame1.path,320*0.75)
        
        cv2.imshow("hej2",frame0Vis)
        cv2.waitKey(10)

        # if traveled > 1:
        #         return traveled, overlapHeight
        # else:
        #         return 0,0
    

def thread_transmit_trajectory():
    print("Thread 4: Starting")
    while True:
        transmit_event.wait()    # Wait for new image
        transmit_event.clear()   # Clear event

        # Get data if lock is free
        with path_lock:
            local_data = path_transmit

        # Do stuff here
    





if __name__ == "__main__":
    # format = "%(asctime)s: %(message)s"
    # logging.basicConfig(format=format, level=logging.INFO,
    #                     datefmt="%H:%M:%S")
    # x = Thread(target=thread_function, args=(1,5))
    # x2 = Thread(target=thread_function2, args=(2,sum))
    # x.start()
    # x2.start()

    t1 = Thread(target=thread_get_image_test, daemon=False)
    t1.start()
    t2 = Thread(target=thread_run_model, daemon=False)
    t2.start()
    t3 = Thread(target=thread_path_plan, daemon=False)
    t3.start()

    # import os
    # import sys
    # while(1):
    #     try:
    #         pass
    #     except KeyboardInterrupt:
    #         print("Interrupt")
    #         try:
    #             sys.exit(0)
    #         except:
    #             os._exit(0)
    #t4 = Thread(target=thread_transmit_trajectory, daemon=False)
    #t4.start()


    # with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    #     executor.map((thread_get_image, thread_path_plan, thread_transmit_trajectory), range(3))


    
