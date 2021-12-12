

class Crack:
    # Coordinates of all cracks in raw pixels
    _crack_coordinates_raw = []
    # Coordinates where some coordinates are removed
    #_crack_coordinates = [[0.0,0.0]]
    # Current index of cracks_coordinates
    _index = 0
    # Checks whether a crack is finished
    _is_done = False
    # number of coordinates
    len = 0
    


    def __init__(self,crack_cords) -> None:
        self._crack_coordinates = crack_cords
        self._add_state()
        self.len = len(self._crack_coordinates)
        self._crack_in_next_frame = False
        pass
    
    def __len__(self):
        return len(self._crack_coordinates)

    def __getitem__(self,index):
        return self._crack_coordinates[index]

    def _add_state(self):
        for idx in range(0,len(self._crack_coordinates)):
            self._crack_coordinates[idx].append(False)
        self._crack_coordinates[0][2] = True
        self._crack_coordinates[-1][2] = True

    
    def set_crack_in_next_frame(self):
        self._crack_in_next_frame = True

    def crack_in_next_frame(self):
        return self._crack_in_next_frame

    def get_first_crack(self):
        return self._crack_coordinates[0]
    
    def shift(self):
        self._crack_coordinates[self._index][2] = True

     #def
    def get_coordinates(self):
        return self._crack_coordinates

    def get_last_crack(self):
        return self._crack_coordinates[-1]
    
    def get_current_crack(self):
        return self._crack_coordinates[self._index]

    def repair(self):
        if not (self._crack_coordinates[self._index] == self._crack_coordinates[-1]):
            self._index += 1
            #print(self._index)
        else:
            self._is_done = True
            #print("DONE")
        

    def get_index(self):
        return self._index

    def is_done(self):
        return self._is_done

    # Removes some coordinates to ensure that 
    def _sort_crack():
        pass


