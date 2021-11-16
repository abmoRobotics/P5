import logging
from threading import Thread, Lock, Event
import time
import cv2
import numpy as np

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
    while True:
        # Do stuff here

        # Set data if lock is free 
        with img_lock:
            img_segmented = 0
            img_event.set()


def thread_path_plan():
    while True:
        img_event.wait()    # Wait for new image
        img_event.clear()   # Clear event

        # Get data if lock is free
        with img_lock:
            local_img = img_segmented

        # DO STUFF HERE

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


    
