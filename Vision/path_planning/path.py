from crack import Crack as cr
import cv2
import math

HEIGHT = 480
WIDTH = 320
INCREMENT = 0.2 # 20% of 1m = 20cm 
PIXEL_INCREMENT = HEIGHT*INCREMENT

class Path():
    # Final path to take
    path = []
    # Pixel on the y-axis where the next frame begins
    next_frame = 480
    # all cracks done
    cracks_done = False
    # List of cracks
    cracks = [cr]
    def __init__(self) -> None:
        self.cracks = []
        pass
    
    # Add crack to path planning
    def add_crack(self, crack: cr) -> cr:
        # Check whether input data is right format
        if not isinstance(crack, cr):
            raise TypeError("Input type must be crack")
        else:
            self.cracks.append(crack)
    
   
    def cracks_done(self):
        length = len(self.cracks)
        counter = 0
        
        for cracker in self.cracks:
            if cracker.is_done():
                counter = counter + 1

        if (counter == length):
            return True
        else:
            return False



    # Get crack with largest y-pixel value.
    def _largest_y_value(self):
         # Find start point
        max_pixel = HEIGHT
        # Starting object
        obj_index = 0
        for idx, crack in enumerate(self.cracks):

            # Get the last crack coordinates that has been repaired
            last_repaired_coordinate = crack.get_current_crack()
            # Check whether y pixel is less than previous
            if max_pixel > last_repaired_coordinate[1]:
                max_pixel = last_repaired_coordinate[1]
                obj_index = idx

        return max_pixel, obj_index



    # Calculates the path
    def find_path(self):
        
        # Path plan until next frame is ready
        while not self._next_frame_ready() and not self.cracks_done():
            print(self.cracks_done())
            # Get the object where the first crack begins
            max_pixel, obj_index = self._largest_y_value()

            #while not self.cracks[obj_index].is_done():
            print(self.cracks[obj_index].get_index())
            print(self.cracks[obj_index].len)
            for idx in range(
                self.cracks[obj_index].get_index(), # Get the current crack not repaired
                self.cracks[obj_index].len          # Run for loop until last object is reached
                ):
                #print(self.cracks[obj_index]._index)
                max_pixel2, obj_index2 = self._largest_y_value()
                if (((self.cracks[obj_index].get_current_crack()[1]) > (max_pixel2 + PIXEL_INCREMENT)) or (self.cracks[obj_index]._is_done)):
                    self.cracks[obj_index].shift()
                    self.cracks[obj_index2].shift()
                    obj_index = obj_index2
                    break
                else:
                    self.path.append(self.cracks[obj_index].get_current_crack())
                    self.cracks[obj_index].repair()

    # Checks whether the next frame is ready
    def _next_frame_ready(self):
        max_pixel, obj_index = self._largest_y_value()
        if (max_pixel > self.next_frame):
            return True
        else: 
            return False


a = []
b = []
for i in range(0,201):
    a.append([1,5+i*2])
    b.append([100,50+i*2])


c1 = cr(a)
c2 = cr(b)

p1 = Path()
p1.add_crack(c1)
p1.add_crack(c2)



path = p1.find_path()

# import numpy as np
# blank_image = np.zeros((HEIGHT,WIDTH,3), np.uint8)

# for i in range(0,len(p1.path)-1):
#     x, y = p1.path[i][0], p1.path[i][1]
#     x1, y1 = p1.path[i+1][0], p1.path[i+1][1]

#     n = i/255
#     n = math.floor(n)
#     if ((n%2) == 0):
#         color = i%255
#     else:
#         color = 255 - (i%255)

#     cv2.line(blank_image, (x, y), (x1, y1), (color, color, 0), thickness=3, lineType=8)

    

# while 1:
#     cv2.imshow("hej",blank_image)
#     cv2.waitKey(20)
