from .tile import Tile

class Car():
    
    def __init__(self, car_ID, orientation, col, row, length):

        self.id = car_ID
        self.orientation = orientation
        self.row = int(row)
        self.col = int(col)
        self.length = int(length)
        self.tiles = []


    def occupies_tiles(self, dimension):
        """
        Creates list of tiles occupied by car
        """
        
        self.tiles.clear()
        tile_ID = int((self.row - 1) * dimension + self.col)
        self.tiles.append(tile_ID)
        
        # add tiles for horizontal car
        if self.orientation == "H":
            self.tiles.append(int(tile_ID + 1))
            # add extra tile if car has length 3
            if self.length == 3:
                self.tiles.append(int(tile_ID + 2))
        # add tiles for vertical car
        else:
            self.tiles.append(int(tile_ID + dimension))
            # add extra tile if car has length 3
            if self.length == 3:
                self.tiles.append(int(tile_ID + 2 * dimension))

    
    def update_position(self, move, dimension):
        """
        Updates car row and column
        """
        # perform move for either horizontal or vertical car
        if self.orientation == "H":
            self.col += move
        else:
            self.row += move

        # recalculate tiles occupied by car
        self.occupies_tiles(dimension)
