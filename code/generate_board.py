from .classes.game import Game
from .classes.car import Car
from .classes.tile import Tile

from .algorithms.baseline_algorithm import Baseline

from random import choice
from math import ceil
import csv

class GenerateBoard:

    def __init__(self, board_size, game_number):
        self.board_size = int(board_size)
        self.game_number = int(game_number)


        while True:
            self.tiles = {}
            self.load_tiles()
            self.tiles_occupied = 0
            # place all the cars
            self.cars = []
            self.generate_cars()

            # make output csv file
            self.get_configuration()
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

        # set the tiles car X is on to occupied
        car_x = Car(car_id_x, orientation_x, col_x, row_x, length_x)
        car_x.occupies_tiles(self.board_size)
        for tile in car_x.tiles:
            self.tiles[tile].set_occupied()
            self.tiles_occupied += 1

        # add car X to the list of cars
        self.cars.append([car_id_x,orientation_x,col_x,row_x,length_x])

        if self.board_size == 6:
            car_amount = choice(range(9,15))
        elif self.board_size == 9:
            car_amount = choice(range(20, 26))
        elif self.board_size == 12:
            car_amount = choice(range(30,50))
        
        print(f"aantal autos: {car_amount}")

        # generate the rest of the cars
        for i in range(car_amount - 1): # NOG AANPASSEN, AANTAL AUTO'S NOG BEPALEN
            if self.tiles_occupied >= len(self.tiles) * 0.75:
                break
            
            car_id = None
            if i < 23:
                car_id = chr(i + 65)
            elif 23 <= i < 25:
                car_id = chr(i + 66)
            elif i >= 25:
                car_id = 'A' + chr(i -25 + 65)
            
            orientation = choice(["H", "V"])
            length = choice([2, 3])

            # get the column and row
            j = 0
            while True:
                j += 1
                if j >= 100:
                    print(f"autos geplaats: {len(self.cars)}")
                    break
                
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
                        self.tiles_occupied += 1

                    # add the car to the list of cars
                    self.cars.append([car_id,orientation,col,row,length])
                    break
                # else:
                #     als ie false is
                #     voeg toe aan niet mogelijk lijst, zorg dat ie die niet nog een keer pakt

    def check_placement(self, orientation, length, col, row):
        """
        Check if the car is placed on already occupied tiles
        """
        tile_id = col + (row - 1) * self.board_size

        if orientation == 'H':
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
        Write the configuration of the game to a gameboard file
        """
        with open(f'data/gameboards/Rushhour{self.board_size}x{self.board_size}_{self.game_number}.csv', 'w', newline = '') as outputfile:
            writer = csv.writer(outputfile)
            writer.writerow(["car", "orientation", "col", "row", "length"])
            writer.writerows(self.cars)

    def check_solvability(self):
        print("checking if board is correct")
        game = Game(self.board_size, self.game_number)
        print(game.give_board())
        algorithm = Baseline(self.board_size, self.game_number)
        command_count = 0

        while True:
            command_string = algorithm.get_command()
            command_count += 1
            
            # check if move is valid
            command = command_string.split(",")
            
            if not game.valid_move(*command):
                continue
            
            game.move(*command)
            # exit when game is won
            if game.game_won():
                return True
            
            if command_count >= 3000000:
                print("unsolvable board")
                print(game.give_board())
                input()
                break

        return False
