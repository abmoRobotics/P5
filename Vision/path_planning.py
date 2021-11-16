import logging
from threading import Thread, Lock, Event
import time
import numpy as np
import cv2
import numpy as np
import concurrent.futures
from imageAligner import imageAlignerCPU
from path_planning import frame
# import torchvision
# from torchvision import transforms
# import albumentations as A

# from vimba import *
# from utils.utils import load_model
# from albumentations.pytorch import ToTensorV2
# import torch
from utils.features import process_image
from path_planning.frame import Frame
from path_planning.crack import Crack
from path_planning.path_planning import (find_path, visualize)
#Transforms
# detect_transform = A.Compose(
#         [
#             A.Resize(height=480, width=320),
#             A.Normalize(
#                 mean=[0.0, 0.0, 0.0],
#                 std=[1.0, 1.0, 1.0],
#                 max_pixel_value=255.0,
#             ),
#             ToTensorV2(),
#         ],
#     )
# DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
# # Load the trained model
# model = load_model("model/crack500BrightnessAugmentation.pth.tar")

# Parameters
SIZE = 480, 320

# Locks
img_lock = Lock()
path_lock = Lock()

# Events    
img_event = Event()
transmit_event = Event()

# Global variables
img_segmented = np.zeros(SIZE, dtype=np.uint8)
path_transmit = []


def thread_get_image():
    print("Thread1")
    
    # with Vimba.get_instance() as vimba:
    #     with vimba.get_camera_by_id("50-0536877557") as cam:
    #         while(1):
    #             # Get frame from camera
    #             frame = cam.get_frame()
    #             frame.convert_pixel_format(PixelFormat.Bgr8)
    #             frame = frame.as_opencv_image
    #             augmentented = detect_transform(image=frame)
    #             data = augmentented["image"].to(device=DEVICE)
    #             data = torch.unsqueeze(data,0)
    #             output = torch.sigmoid(model(data))
    #             output = torch.squeeze(output)
    #             preds = (output > 0.5).float()
    #             # preds = closing(preds.cpu().numpy())
    #             # preds = skeletonization(preds)
    #             # preds = (preds*255).astype(np.uint8)
    #             cv2.imshow("preview", preds.cpu().numpy())
    #             cv2.imshow("normal", frame)
    #             cv2.waitKey(1)
    #             # Set data if lock is free 
    #             with img_lock:
    #                 img_segmented = 0
    #                 img_event.set()


def thread_path_plan():
    print("Thread2")
    img_old_seg = 0

    while True:
        img_event.wait()    # Wait for new image
        img_event.clear()   # Clear event

        # Get data if lock is free
        with img_lock:
            local_img = img_segmented

        sorted_cracks = process_image(local_img)

        if not img_old_seg == 0:
            traveled, overlapHeight = imageAlignerCPU(img_old_seg, local_img)
            img_old_seg = local_img
            

        frame1 = Frame()

        for crack in sorted_cracks:
            frame1.add_crack(Crack(crack))

        # Set data if lock is free
        with path_lock:
            path_transmit = find_path(frame1)
            transmit_event.set()    # Set event true

        if traveled > 1:
                return traveled, overlapHeight
        else:
                return 0,0
    

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
    t2 = Thread(target=thread_path_plan, daemon=False)
    t2.start()
    t3 = Thread(target=thread_transmit_trajectory, daemon=False)
    t3.start()


    # with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    #     executor.map((thread_get_image, thread_path_plan, thread_transmit_trajectory), range(3))


    
