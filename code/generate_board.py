from .classes.game import Game
from .classes.car import Car
from .classes.tile import Tile

from .algorithms.random import Random

from random import choice
from math import ceil
import csv

class GenerateBoard:
    """
    This class is used to implement an algorithm that generates a solvable Rushhour game board.
    Parameters for initialisation: board_size(int), game_number(int)
    """

    def __init__(self, board_size, game_number):
        self.board_size = int(board_size)
        self.game_number = int(game_number)
        
        # get the amount of cars
        if self.board_size == 6:
            self.car_amount = choice(range(9,15))
        elif self.board_size == 9:
            self.car_amount = choice(range(20, 26))
        elif self.board_size == 12:
            self.car_amount = choice(range(30,50))

        # generate game boards until you get a solvable one
        while True:
            # load tiles
            self.tiles = {}
            self.load_tiles()
            self.tiles_occupied = 0

            # place all the cars
            self.cars = []
            self.generate_cars()

            # make output csv file
            self.get_configuration()
            # stop if the game board is solvable
            if self.check_solvability():
                break


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
        print("generating cars")
        # generate car X
        car_id_x = 'X'
        orientation_x = 'H'
        col_x = 1
        row_x = ceil(self.board_size / 2)
        length_x = 2

        # add car X to the list of cars and set the tiles car X is on to occupied 
        self.set_tile_occupancy(car_id_x, orientation_x, col_x, row_x, length_x)

        # generate the rest of the cars
        for i in range(self.car_amount - 1):
            # if more than 3/4 of the board is occupied, stop
            if self.tiles_occupied >= len(self.tiles) * 0.75:
                break
            
            # get car id
            if i < 23:
                car_id = chr(i + 65)
            # skip X
            elif 23 <= i < 25:
                car_id = chr(i + 66)
            # start double letters
            elif i >= 25:
                car_id = 'A' + chr(i -25 + 65)
            
            orientation = choice(["H", "V"])
            length = choice([2, 3])

            # place the car in a column and row on the board
            # if you are not able to place it in 100 tries, stop
            j = 0
            while j < 100:
                j += 1
                
                # get column and row
                if orientation == 'H':
                    col = choice(range(1, self.board_size - (length - 1) + 1))
                    row = choice(range(1, self.board_size + 1))
                else:
                    col = choice(range(1, self.board_size + 1))
                    row = choice(range(1, self.board_size - (length - 1) + 1))

                # make sure the car is not placed on already occupied tiles
                if self.check_placement(orientation, col, row, length):
                    self.set_tile_occupancy(car_id, orientation, col, row, length)
                    break


    def set_tile_occupancy(self, car_id, orientation, col, row, length):
        """
        Sets the tiles a car is standing on to occupied and adds the car to self.cars
        """
        # set the tiles the car is on to occupied
        car = Car(car_id, orientation, col, row, length)
        car.occupies_tiles(self.board_size)
        for tile in car.car_attributes()["tiles"]: 
            self.tiles[tile].set_occupied()
            self.tiles_occupied += 1

        # add the car to the list of cars
        self.cars.append([car_id,orientation,col,row,length])


    def check_placement(self, orientation, col, row, length):
        """
        Checks if the car is placed on already occupied tiles
        """
        # get tile id
        tile_id = col + (row - 1) * self.board_size

        # if the car is on already occupied tiles, return False
        if orientation == 'H':
            # a horizontal car cannot be in the same row as car X
            if row == ceil(self.board_size / 2):
                return False
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
        Writes the configuration of the game to a csv file
        """
        with open(f'data/gameboards/Rushhour{self.board_size}x{self.board_size}_{self.game_number}.csv', 'w', newline = '') as outputfile:
            writer = csv.writer(outputfile)
            writer.writerow(["car", "orientation", "col", "row", "length"])
            writer.writerows(self.cars)


    def check_solvability(self):
        """
        Checks if the generated board is solvable using the Random algorithm
        """
        print("checking if board is correct")
        game = Game(self.board_size, self.game_number)
        algorithm = Random(game)
        command_count = 0

        # execute commands until game is won, or there have been more than 100,000 moves
        while True:
            # get command from the Random algorithm and execute it
            command_string = algorithm.get_command()
            command_count += 1
            command = command_string.split(",")
            game.move(*command)
            
            # exit when game is won
            if game.game_won():
                return True
            
            # if there is no solution after 100,000 moves, stop
            if command_count >= 100000:
                break
        return False