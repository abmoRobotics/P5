from frame import Frame
from crack import Crack

# Funktion der transfer information fra en frame
# INPUTS:
    # 1. frame 1
    # 2. frame 2
    # 3. hvor mange frames de er forskudt
    # 4.   
# 
def transfer_frame(frame1: Frame, frame2: Frame,):
    pass



# Determines which cracks must be transfered
def map_cracks(frame1: Frame, frame2: Frame, offset: int):
    '''Maps cracks from frame 1 to frame 2'''

    # First the function maps crack from frame 1 to frame 2.
    mapped_cracks = []
    for i, crack_frame1 in enumerate(frame1.cracks):
        if crack_frame1.crack_in_next_frame():
            x_val_frame1 = (crack_frame1.get_last_crack())[0]
            index = 0
            min_val = 999
            for idx, crack_frame2 in enumerate(frame2.cracks):
                x_val_frame2 = (crack_frame2.get_first_crack())[0]
                frame_diff = abs(x_val_frame2-x_val_frame1) 
                if frame_diff < min_val:
                    min_val = frame_diff
                    index = idx
            mapped_cracks.append({"old_frame": i, "new_frame": index})

    # Secondly the function marks the transfered "repaired" cracks from frame 1 to frame 2 and marks them as repaired
    for cracks in mapped_cracks:
        old_crack_id = cracks['old_frame']
        new_crack_id = cracks['new_frame']

        frame1_current_crack = frame1.cracks[old_crack_id].get_current_crack()
        while not frame2.cracks[new_crack_id].is_done():
            if ((frame2.cracks[new_crack_id].get_current_crack())[1] <= frame1_current_crack[1] - offset):
                # Marks the current point in the crack as "repaired"
                frame2.cracks[new_crack_id].repair()
            else:
                # Indicates that this is the start/end of a crack
                frame2.cracks[new_crack_id].shift()
                break

    return mapped_cracks






"""
class map_cracks():
    '''Maps cracks from frame 1 to frame 2'''
    def __init__(self, frame1: Frame, frame2: Frame, offset: int) -> None:
        self.map = map_cracks(frame1,frame2,offset)
        pass

    
    def map_cracks(frame1: Frame, frame2: Frame, offset: int):
        '''Maps cracks from frame 1 to frame 2'''
        mapped_cracks = []
        for i, crack_frame1 in enumerate(frame1.cracks):
            if crack_frame1.crack_in_next_frame():
                x_val_frame1 = (crack_frame1.get_last_crack())[0]
                index = 0
                min_val = 999
                for idx, crack_frame2 in enumerate(frame2.cracks):
                    x_val_frame2 = (crack_frame2.get_first_crack())[0]
                    frame_diff = abs(x_val_frame2-x_val_frame1) 
                    if frame_diff < min_val:
                        min_val = frame_diff
                        index = idx
                mapped_cracks.append({"old_frame": i, "new_frame": index})
        return mapped_cracks
"""