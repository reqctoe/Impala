from .tile import Tile

class Car():
    
    def __init__(self, car_ID, orientation, col, row, length):
        self.id = car_ID
        self.orientation = orientation
        self.row = int(row)
        self.col = int(col)
        self.length = int(length)
        self.tiles = []

        # print(self.length)

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

        # print("wu")

    def occupation(self, tiles):
        print(self.tiles)
        for tile in self.tiles:
            tiles[tile].set_occupied()
            # print(tile)
        for tile in tiles:
            print(tiles[tile].occupied)
    
    def update_position(self, move, dimension):
        if self.orientation == "H":
            self.col += move
        else:
            self.row += move

        print(self.row, self.col)

        self.occupies_tiles(dimension)
