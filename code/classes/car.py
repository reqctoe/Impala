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
        self.tiles.clear()
        tile_ID = int((self.row - 1) * dimension + self.col)
        self.tiles.append(tile_ID)
        if self.orientation == "H":
            self.tiles.append(int(tile_ID + 1))
            if self.length == 3:
                self.tiles.append(int(tile_ID + 2))
        else:
            self.tiles.append(int(tile_ID + dimension))
            if self.length == 3:
                self.tiles.append(int(tile_ID + 2 * dimension))


    def occupation(self, tiles):
        for tile in self.tiles:
            tiles[tile].set_occupied()
    
    def update_position(self, move, dimension):
        if self.orientation == "H":
            self.col += move
        else:
            self.row += move

        self.occupies_tiles(dimension)
