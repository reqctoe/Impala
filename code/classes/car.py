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
        tile_ID = int((self.row - 1) * dimension + self.col)
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

    def update_position(self, move):
        if self.orientation == "H":
            self.col += move
        else:
            self.row += move


    # in game.py
    def game_won(self):
        win_tile = (ceil(dimension / 2) - 1) * dimension + dimension
        self.winning_tile = self.tiles[win_tile]

        if self.winning_tile in self.cars[X].tiles:
            return True
        return False

    def current_board(self):
        self.tile_occupation = {}

        for car in self.cars:
            for tile in car.tiles:
                self.tile_occupation[tile] = car.id
        
        for tile in self.tiles:
                
            if self.tile_occupation[tile]:
                print(self.tile_occupation[tile])
            else:
                print("_")

            if tile.id % self.dimension == 0:
                print("\n")
