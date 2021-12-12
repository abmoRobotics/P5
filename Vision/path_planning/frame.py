from path_planning.crack import Crack
import json


class Frame():
    # Final path to take
    # path = []
    # Pixel on the y-axis where the next frame begins
    next_frame = 480
    KEEP_EVERY_X_PIXEL = 3
    # all cracks done
    cracks_done = False
    # List of cracks
    #cracks = [cr]

    def __init__(self) -> None:
        self.path = []
        self.raw_cracks: Crack = []
        self.cracks: Crack  = []
        self.frame_time = 0
        pass
    def __len__(self):
        return len(self.cracks)
    # Add crack to path planning
    def add_crack(self, crack: Crack) -> Crack:
        # Check whether input data is right format
        if not isinstance(crack, Crack):
            raise TypeError("Input type must be crack")
        else:       
            # check if crack is in next frame
            last_crack = crack.get_last_crack()
            #print(last_crack[1])
            if ((crack.get_last_crack())[1] > self.next_frame):
                crack.set_crack_in_next_frame()

            # Add crack to frame
            self.raw_cracks.append(crack)
    # 
    def cracks_done(self):
        length = len(self.raw_cracks)
        counter = 0
        
        for cracker in self.raw_cracks:
            if cracker.is_done():
                counter = counter + 1

        if (counter == length):
            return True
        else:
            return False

    # Get crack with largest y-pixel value.
    def _largest_y_value(self):
        # Find start point
        max_pixel = 99999
        # Starting object
        obj_index = 0
        for idx, crack in enumerate(self.cracks):

            # Get the last crack coordinates that has been repaired
            if not crack.is_done():
                last_repaired_coordinate = crack.get_current_crack()
                # Check whether y pixel is less than previous
                if max_pixel > last_repaired_coordinate[1]:
                    max_pixel = last_repaired_coordinate[1]
                    obj_index = idx

        return max_pixel, obj_index

    # Checks whether the next frame is ready
    def _next_frame_ready(self):
        max_pixel, obj_index = self._largest_y_value()
        if (max_pixel > self.next_frame):
            return True
        else: 
            return False

    def _remove_pixels(self):
        resolution = self.KEEP_EVERY_X_PIXEL
        
        self.cracks.clear()

        for crack in self.raw_cracks:
            temp_crack = []
            for idx in range(0, len(crack), resolution):
                temp_crack.append(crack[idx])
            
            c = Crack(temp_crack)
            self.cracks.append(c)
            


    def get_json_array(self):
        json_array = []

        for path in self.path:
            Data = {
                "Position": {
                    "X": path[0],
                    "Y": path[1]
                    },
                "Time": {"Detected": self.frame_time},
                "Crack": {"DetectionIndex": path[2]}
                }
            
            json_array.append(Data)
        
        return json_array

    def find_path(self):
        # Remove path if already calculated
        self.path.clear()
        # Save evey third pixel
        self._remove_pixels()
        PIXEL_INCREMENT = 96*1.55
        while not self._next_frame_ready() and not self.cracks_done():
            
            # Get the object where the first crack begins
            max_pixel, obj_index = self._largest_y_value()
            
            #while not frame.cracks[obj_index].is_done():
            for idx in range(
                self.cracks[obj_index].get_index(), # Get the current crack not repaired
                self.cracks[obj_index].len          # Run for loop until last object is reached
                ):
                max_pixel2, obj_index2 = self._largest_y_value()
                # If next frame is ready exit for loop and continue with next frame
                if self._next_frame_ready():
                    break
                # Check if should shift to another crack
                elif (((self.cracks[obj_index].get_current_crack()[1]) > (max_pixel2 + PIXEL_INCREMENT)) or (self.cracks[obj_index]._is_done)):
                    self.cracks[obj_index].shift()
                    self.path.append(self.cracks[obj_index].get_current_crack())
                    #print("From", self.cracks[obj_index].get_current_crack())
                    self.cracks[obj_index2].shift()
                    #print("To", self.cracks[obj_index2].get_current_crack())
                    obj_index = obj_index2
                    break
                # Point will be repaired
                else:
                    self.path.append(self.cracks[obj_index].get_current_crack())
                    self.cracks[obj_index].repair()
            

    def set_frame_time(self, t):
        self.frame_time = t

    def get_frame_time(self):
        return self.frame_time
