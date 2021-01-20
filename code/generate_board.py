from .classes.game import Game
from .classes.car import Car
from .classes.tile import Tile

from random import choice
from math import ceil
import csv

class GenerateBoard:

    def __init__(self, board_size, game_number):
        self.board_size = int(board_size)
        self.game_number = int(game_number)

        self.tiles = {}
        self.load_tiles()

        # place all the cars
        self.cars = []
        self.generate_cars()

        # make output csv file
        self.get_configuration()

    def load_tiles(self):
        """
        Load tiles
        """

        # create all tile objects with occupied false
        for row in range(1, self.board_size + 1):
            for col in range(1, self.board_size + 1):
                id = ((row - 1) * self.board_size) + col
                new_tile = Tile(id, row, col)
                self.tiles[new_tile.id] = new_tile

    def generate_cars(self):
        """
        Generates a list of cars and their position on the board
        """
        # generate car X
        car_id_x = 'X'
        orientation_x = 'H'
        col_x = 1
        row_x = ceil(self.board_size / 2)
        length_x = 2

        # set the tiles car X is on to occupied
        car_x = Car(car_id_x, orientation_x, col_x, row_x, length_x)
        car_x.occupies_tiles(self.board_size)
        for tile in car_x.tiles:
            self.tiles[tile].set_occupied()

        # add car X to the list of cars
        self.cars.append([car_id_x,orientation_x,col_x,row_x,length_x])

        # generate the rest of the cars
        for i in range(choice(range(5,10))): # NOG AANPASSEN, AANTAL AUTO'S NOG BEPALEN
            car_id = chr(i + 65)
            orientation = choice(["H", "V"])
            length = choice([2, 3])

            # get the column and row
            while True:
                if orientation == 'H':
                    col = choice(range(1, self.board_size - (length - 1) + 1))
                    row = choice(range(1, self.board_size + 1))
                else:
                    col = choice(range(1, self.board_size + 1))
                    row = choice(range(1, self.board_size - (length - 1) + 1))

                # make sure the car is not placed on already occupied tiles
                if self.check_placement(orientation, length, col, row):
                    # set the tiles the car is on to occupied
                    car = Car(car_id, orientation, col, row, length)
                    car.occupies_tiles(self.board_size)
                    for tile in car.tiles:
                        self.tiles[tile].set_occupied()

                    # add the car to the list of cars
                    self.cars.append([car_id,orientation,col,row,length])
                    break

    def check_placement(self, orientation, length, col, row):
        """
        Check if the car is placed on already occupied tiles
        """
        tile_id = col + (row - 1) * self.board_size

        if orientation == 'H':
            for tile in range(tile_id, tile_id + length):
                if self.tiles[tile].occupied:
                    return False
        else:
            for tile in range(tile_id, tile_id + (length - 1) * self.board_size + 1, self.board_size):
                if self.tiles[tile].occupied:
                    return False
        
        return True

    def get_configuration(self):
        """
        Write the configuration of the game to a gameboard file
        """
        with open(f'data/gameboards/Rushhour{self.board_size}x{self.board_size}_{self.game_number}.csv', 'w', newline = '') as outputfile:
            writer = csv.writer(outputfile)
            writer.writerow(["car", "orientation", "col", "row", "length"])
            writer.writerows(self.cars)
