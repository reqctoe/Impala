from .breadth_first import BreadthFirst
from code.classes.game import Game

import copy


class DepthFirst(BreadthFirst):

    def get_next_state(self):
        """
        Next node retrieval in a LIFO order
        """
        key = self.state_keys.pop()
        
        print(f"Stack length: {len(self.state_keys)}")
        
        return self.states[key]

   