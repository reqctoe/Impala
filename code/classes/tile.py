
# DIT MOET WORDEN GEINPORT VOOR DE GAME CLASS
from csv import DictReader

class Tile:
    """This class is used to create tiles for the Rush Hour board.
      Parameters for initialisation: row(int), col(int). Where row starts
      counting from the top and col from the left."""


    def __init__(self, id, row, col):
        self.id = id
        self.row = row
        self.col = col
        self.ocupied = False
    
    def set_occupied(self):
        """Sets the tiles occupied variable to True."""

        self.occupied = True

    def set_unoccupied(self):
        """Sets the tiles occupied variable to False."""

        self.occupied = False



    # DEZE IS VOOR IN DE GAME CLASS
    def load_tiles(self, data, board_size):

        self.tiles = {}
        
        # add all tiles with occupied to false
        for row in board_size:
            for col in board_size:
                id = ((row - 1) * board_size) + col
                new_tile = Tile(id, row, col)
                self.tiles[new_tile.id] = new_tile

        # set tiles that have a car on them as occupied
        with open(FILE, "r") as data: # HIER EVEN DE GOEIE FILENAAM TOEVOEGEN IN DE GAME CLASS
            data_dict = DictReader(data)

        for car in data_dict:
            # set first tile to occupied
            id = ((car[row] - 1) * board_size) + car[col]   # hier wordt ervan uitgegaan dat de header van de file klopt
            tile = self.tiles[id]
            tile.occupied = True

            # TODO set second tile to occupied

            # TODO if length is 3 set 3rd tile to occupied

