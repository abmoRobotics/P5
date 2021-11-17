
from path_planning.frame import Frame
from path_planning.crack import Crack
import cv2
import math
import random
import numpy as np

HEIGHT = 320
WIDTH = 480
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



