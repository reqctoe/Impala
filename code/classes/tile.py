class Tile:
    """
    This class is used to create tiles for the Rush Hour board.
    Parameters for initialisation: row(int), col(int). Where row starts
    counting from the top and col from the left.
    """


    def __init__(self, id, row, col):
        self.id = id
        self.row = row
        self.col = col
        self.occupied = False
    
    def set_occupied(self):
        """
        Sets the tiles occupied variable to True.
        """

        self.occupied = True

    def set_unoccupied(self):
        """
        Sets the tiles occupied variable to False.
        """

        self.occupied = False

    def get_occupied(self):
        """
        Gives occupation
        """
        return self.occupied

    def tile_attributes(self):
        """
        Gives all attributes for the class in a dictionary
        """
        return {
            "id": self.id,
            "row": self.row,
            "col": self.col,
        }

