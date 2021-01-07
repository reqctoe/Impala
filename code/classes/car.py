from tile import Tile

class Car():
    
    def __init__(self, car_ID, orientation, col, row, length):
        self.id = car_ID
        self.orientation = orientation
        self.row = row
        self.col = col
        self.length = length
        self.tiles = []


    def occupies_tiles(self, dimension, tiles):
        tile_ID = int((self.row - 1) * 6 * dimension + self.col)
        car_tiles = [tile_ID]
        if self.orientation == "H":
            car_tiles.append(int(tile_ID + 1))
            if self.length == 3:
                car_tiles.append(int(tile_ID + 2))
        else:
            car_tiles.append(int(tile_ID + dimension))
            if self.length == 3:
                car_tiles.append(int(tile_ID + 2 * dimension))
        
        for tile in car_tiles:
            self.tiles.append(tiles[tile])
            tiles[tile].set_occupied()

    def update_position
    
    
    
    # def occupies_tiles(self, dimension):
    #     tile = 1
    #     while True:
    #         if tile == 1:
    #             ID = int((self.row - 1) * 6 * dimension + self.col)
    #             row = self.row
    #             col = self.col
    #             tile += 1
    #         elif tile == 2:
    #             if self.orientation == 'H':
    #                 ID += 1
    #                 col += 1
    #             else:
    #                 ID += dimension
    #                 row += 1
    #             tile += 1
    #         elif tile == 3:
    #             if self.length == 3:
    #                 if self.orientation == 'H':
    #                     ID += 1
    #                     col += 1
    #                 else:
    #                     ID += dimension
    #                     row += 1
    #             else:
    #                 break

    #         tile = [ID, row, col]
    #         self.tiles.append(Tile(*tile))