
class Crack:
    # Coordinates of all cracks in raw pixels
    _crack_coordinates_raw = []
    # Coordinates where some coordinates are removed
    _crack_coordinates = [[0.0,0.0]]
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
        pass
    
    def _add_state(self):
        for idx in range(0,len(self._crack_coordinates)):
            self._crack_coordinates[idx].append(False)
        self._crack_coordinates[0][2] = True
        self._crack_coordinates[-1][2] = True

    def get_first_crack():
        pass
    
    def shift(self):
        self._crack_coordinates[self._index][2] = True

     #def


    def get_last_crack():
        pass
    
    def get_current_crack(self):
        return self._crack_coordinates[self._index]

    def repair(self):
        if not (self._crack_coordinates[self._index] == self._crack_coordinates[-1]):
            self._index += 1
            print(self._index)
        else:
            self._is_done = True
            print("DONE")
        

    def get_index(self):
        return self._index

    def is_done(self):
        return self._is_done

    # Removes some coordinates to ensure that 
    def _sort_crack():
        pass


