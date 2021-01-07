from tile import Tile
from car import Car

from math import ceil

class Game():
    def __init__(self, board_size, board_file):

        self.board_size = board_size

        # tiles is a dictionary that maps a tile number to the corresponding tile object
        self.tiles = {}
        # cars is a dictionary that maps a car letter to the corresponding car object
        self.cars = {}

        # load cars and tiles
        self.load_tiles()
        self.load_cars(board_file)

        # set winning tile
        win_tile = (ceil(self.board_size / 2) - 1) * self.board_size + self.board_size
        self.winning_tile = self.tiles[win_tile]

    def load_tiles(self):
        """
            Load tiles
        """

        # add all tiles with occupied to false
        for row in self.board_size:
            for col in self.board_size:
                id = ((row - 1) * self.board_size) + col
                new_tile = Tile(id, row, col)
                self.tiles[new_tile.id] = new_tile

    def load_cars(self, board_file):
        """
        Load cars from file
        """
        with open(board_file) as f:
            for line in f:
                car_line = f.readline().split(",")
                self.cars[car_line[0]] = Car(*car_line)

    def current_board(self):
        pass

    def valid_move(self, car_id, move):
        """
        Checks if the move is valid
        """
        car = self.cars[car_id]

        # check if you don't move through any cars or walls, return false if you do
        # if the car's orientation is horizontal, only look through its row 
        if car.orientation == 'H':
            # check if you don't move through walls
            if 1 > car.row + move >= self.board_size:
                return False

            # TODO: ook werkend krijgen voor negatieve bewegingen
            # check if you don't move through cars
            for i in range(1, move+1):
                if self.tiles[((car.row - 1) * self.board_size) + i].occupied:
                    return False
        # if it is vertical, only look through its column
        else:
            if 1 > car.col + move > self.board_size:
                return False
            for i in range(1, move+1):
                if self.tiles[((i - 1) * self.board_size) + car.col].occupied == False:
                    return False
        
        return True

        # # if the orenientation of the car is horizontal, check if the move is in the same row
        # if car.orientation == 'H' & :
        #     return 
        # # if the orientation is vertical, check if the move is in the same column
        # elif car.orientation == 'V':

    def move(self, car, move):
        """
        Move a car to a different possition
        """
        # set current tiles to unoccupied
        for tile in self.cars[car.id].tiles:
            tile.set_unoccupied()

        # set new position car 
        self.cars[car.id].update_position(move)

        # set tiles to occupied 
        for tile in self.cars[car.id].tiles:
            tile.set_occupied()

    def game_won(self):
        """
        Checks if the red car (with id X) is in front of the exit
        """
        if self.winning_tile in self.cars['X'].tiles:
            return True
        return False
