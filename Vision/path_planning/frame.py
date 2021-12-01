from path_planning.crack import Crack as cr

class Frame():
    # Final path to take
    # path = []
    # Pixel on the y-axis where the next frame begins
    next_frame = 320*0.75
    # all cracks done
    cracks_done = False
    # List of cracks
    #cracks = [cr]

    def __init__(self) -> None:
        self.path = []
        self.cracks: cr = []
        self.frame_time = 0
        pass
    
    # Add crack to path planning
    def add_crack(self, crack: cr) -> cr:
        # Check whether input data is right format
        if not isinstance(crack, cr):
            raise TypeError("Input type must be crack")
        else:       
            # check if crack is in next frame
            last_crack = crack.get_last_crack()
            #print(last_crack[1])
            if ((crack.get_last_crack())[1] > self.next_frame):
                crack.set_crack_in_next_frame()

            # Add crack to frame
            self.cracks.append(crack)
   # 
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
    def set_frame_time(self, t):
        self.frame_time = t

    def get_frame_time(self):
        return self.frame_time
