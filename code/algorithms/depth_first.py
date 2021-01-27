from .breadth_first import Breadth_first


class Depth_first(Breadth_first):

    def get_next_state(self):
        """
        Next node retrieval in a LIFO order
        """
        key = self.state_keys.pop()
        
        print(f"Stack length: {len(self.state_keys)}")
        
        return self.states[key]

   