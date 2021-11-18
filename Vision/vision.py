import logging
from multiprocessing import Process, Lock, Event
from multiprocessing.managers import BaseManager
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



def thread_get_image_test(instance,lock,event):
    print("Thread 1: Starting")
    #global img_raw
    cap = cv2.VideoCapture(1)
    # try to get first frame
    if cap.isOpened():
        rval, frame = cap.read()
    else: 
        rval = False
    while rval:
        
        start_time = time.time()
        rval, frame = cap.read()

        lock.acquire()
        instance.set(frame)
        event.set()
        lock.release()
        print("Thread 1:", time.time()-start_time)
        time.sleep(3)

def thread_get_image(data_out, lock_out, event_out):
    print("Thread 1: Starting")
    global img_raw
    with Vimba.get_instance() as vimba:
        with vimba.get_camera_by_id("50-0536877557") as cam:
            while(1):
                start_time = time.time()
                # Get frame from camera
                #time1 = time.time()
                frame = cam.get_frame()
                frame.convert_pixel_format(PixelFormat.Bgr8)
                frame = frame.as_numpy_ndarray()
                #print("FPS: %s", 1/(time.time()-time1))
                
                # Get lock if free
                lock_out.acquire()
                # Set data
                data_out.set(frame)
                # Set next event
                event_out.set()
                # Rel
                lock_out.release()
                
                print("Thread 1:", time.time()-start_time)
                #print("FPS: %s", 1/(time.time()-time1))
                
def thread_run_model(data_in, data_out, lock_in, lock_out, event_in, event_out):

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
    print("Thread 2: Starting")
    img_raw_old = np.zeros(([2, 2]), dtype=np.uint8)
    local_image = 0
    traveled = 0
    while(1):
        event_in.wait()
        event_in.clear()
        start_time = time.time()

        lock_in.acquire()
        local_image = data_in.get().copy()
        lock_in.release()
    

        
        if img_raw_old.any():
            
            new_image = cv2.resize(local_image,(WIDTH,HEIGHT),interpolation=cv2.INTER_AREA)
            new_image = cv2.cvtColor(new_image,cv2.COLOR_BGR2GRAY)
            traveled, overlapHeight = imageAlignerCPU(img_raw_old, new_image)
            

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
        
        img_raw_old = cv2.resize(img_raw_old,(480,320),interpolation=cv2.INTER_AREA)
        img_raw_old = cv2.cvtColor(img_raw_old,cv2.COLOR_BGR2GRAY)
        # Set data if lock is free
         
        lock_out.acquire()
        data_out.set(preds.cpu().numpy())      
        data_out.set_image_offset(traveled)
        event_out.set()         # set event
        lock_out.release()
        

        print("Thread 2: ", time.time()-start_time)

def thread_path_plan(data_in, data_out, lock_in, lock_out, event_in, event_out):
    print("Thread 3: Starting")
    img_old_seg = np.zeros(([2, 2]), dtype=np.uint8)
    old_frame = 0
    traveled = 0

    while True:
        event_in.wait()    # Wait for new image
        event_in.clear()   # Clear event
        start_time = time.time()
        
        # Get data if lock is free
        lock_in.acquire()
        local_img = data_in.get().astype(np.uint8) # get data
        offset = data_in.get_image_offset()
        lock_in.release()
        print("OFFSET: ", offset)
        sorted_cracks = process_image(local_img)
        img_old_seg = local_img
        frame1 = Frame()    
        
        

        for crack in sorted_cracks:
            frame1.add_crack(Crack(crack))
        
        
        if not old_frame == 0:
            #print("hej")
            #print(old_frame.path)
            map_cracks(old_frame,frame1,offset)
        path1 = find_path(frame1)
       
        old_frame = copy.copy(frame1)
        # from path_planning.utils import map_cracks
        # if not old_frame == 0:
        #     map_cracks()
        
        
        # Set data if lock is free
        lock_out.acquire()

        data_out.set(find_path(frame1))
        event_out.set()
        lock_out.release()
        print("Thread 3: ", time.time()-start_time)
        #print("FPS: ", 1/(time.time()-t1))
        frame0Vis = visualize(frame1, frame1.path,320*0.75)
        
        cv2.imshow("hej2",frame0Vis)
        cv2.waitKey(10)
    
def thread_transmit_trajectory(data_in, lock_in, event_in):
    print("Thread 4: Starting") 
    while True:
        event_in.wait()     # Wait for new image
        event_in.clear()    # Clear event
        start_time = time.time()

        # Get data if lock is free
        lock_in.acquire()
        local_data = data_in.get()
        lock_in.release()
        print("Thread 4: ", time.time()-start_time)
        # Do stuff here
        


class dataTransfer:
    def __init__(self) -> None:
        self.data = 0
        self.offset = 0
    def set(self,value):
        self.data = value
    def get(self):
        return self.data
    def set_image_offset(self,value):
        self.offset = value
    def get_image_offset(self):
        return self.offset

if __name__ == "__main__":
    BaseManager.register('dataTransfer', dataTransfer)

    # Locks
    img_raw_lock = Lock()
    img_seg_lock = Lock()
    path_lock = Lock()

    # Events
    img_raw_event = Event()     # Start thread 2
    img_seg_event = Event()     # Start thread 3
    transmit_event = Event()    # Start thread 4
    
    # Manager setup
    manager_raw_img = BaseManager()
    manager_seg_img = BaseManager()
    manager_path = BaseManager()
    
    manager_raw_img.start()
    manager_seg_img.start()
    manager_path.start()
    
    inst_raw_img = manager_raw_img.dataTransfer()
    inst_seg_img = manager_seg_img.dataTransfer()
    inst_path = manager_path.dataTransfer()
    

    
    # Thread initialization
    t1 = Process(target=thread_get_image, args=(
        inst_raw_img,
        img_raw_lock,
        img_raw_event
        ))
    t2 = Process(target=thread_run_model, args=(
        inst_raw_img, 
        inst_seg_img,  
        img_raw_lock, 
        img_seg_lock, 
        img_raw_event,
        img_seg_event,))
    t3 = Process(target=thread_path_plan, args=(
        inst_seg_img, 
        inst_path, 
        img_seg_lock,
        path_lock,
        img_seg_event,
        transmit_event
        ))
    t4 = Process(target=thread_transmit_trajectory, args=(
        inst_path, 
        path_lock, 
        transmit_event
        ))

    processes = [t1,t2,t3,t4]

    for process in processes:
        process.start()
    
    for process in processes:
        process.join()
        
        
