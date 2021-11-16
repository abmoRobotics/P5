import logging
from threading import Thread, Lock, Event
import time
import numpy as np
import cv2
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
#Transforms
detect_transform = A.Compose(
        [
            A.Resize(height=320, width=480),
            A.Normalize(
                mean=[0.0, 0.0, 0.0],
                std=[1.0, 1.0, 1.0],
                max_pixel_value=255.0,
            ),
            ToTensorV2(),
        ],
    )
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
# Load the trained model
model = load_model("model/crack500BrightnessAugmentation.pth.tar")

# Parameters
SIZE = 480, 320,3

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


def thread_get_image():
    print("Thread 1: Starting")
    global img_raw
    with Vimba.get_instance() as vimba:
        with vimba.get_camera_by_id("50-0536877557") as cam:
            while(1):
                time1 = time.time()
                # Get frame from camera
                frame = cam.get_frame()
                frame.convert_pixel_format(PixelFormat.Bgr8)
                frame = frame.as_numpy_ndarray()
                #print("FPS: %s", 1/(time.time()-time1))
                
                with img_raw_lock:
                    img_raw = frame
                    img_raw_event.set()
                
def thread_run_model():
    print("Thread 2: Starting")
    global img_raw
    global img_seg
    while(1):
        img_raw_event.wait()
        img_raw_event.clear()
        time1 = time.time()
        with img_raw_lock:
            local_image = img_raw
        augmentented = detect_transform(image=local_image)
        data = augmentented["image"].to(device=DEVICE)
        data = torch.unsqueeze(data,0)
        output = torch.sigmoid(model(data))
        output = torch.squeeze(output)
        preds = (output > 0.5).float()
        cv2.imshow("preview", preds.cpu().numpy())
        #cv2.imshow("normal", frame)
        cv2.waitKey(1)
        # Set data if lock is free 
        with img_seg_lock:
            img_seg = preds.cpu().numpy()
        print("FPS: %s", 1/(time.time()-time1))
    

def thread_path_plan():
    global img_seg
    global path_transmit
    while True:
        img_seg_event.wait()    # Wait for new image
        img_seg_event.clear()   # Clear event

        # Get data if lock is free
        with img_seg_lock:
            local_img = img_seg

        process_image(local_img)

        # ALIGN AND PATH PLANNING


        # Set data if lock is free
        with path_lock:
            path_transmit = [[2,3],[2,4]]
            transmit_event.set()    # Set event true
    
    

def thread_transmit_trajectory():
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

    t1 = Thread(target=thread_get_image, daemon=False)
    t1.start()
    t2 = Thread(target=thread_run_model, daemon=False)
    t2.start()
    t3 = Thread(target=thread_path_plan, daemon=False)
    t3.start()
    t4 = Thread(target=thread_transmit_trajectory, daemon=False)
    t4.start()


    # with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    #     executor.map((thread_get_image, thread_path_plan, thread_transmit_trajectory), range(3))


    
