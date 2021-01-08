from .tile import Tile
from .car import Car

from math import ceil, floor

class Game():
    def __init__(self, board_size, game_number):

        self.board_size = int(board_size)
        self.tile_occupation = {}
        self.board = []

        # tiles is a dictionary that maps a tile number to the corresponding tile object
        self.tiles = {}
        # cars is a dictionary that maps a car letter to the corresponding car object
        self.cars = {}

        # load cars and tiles
        self.load_tiles()
        board_file = f"data/gameboards/Rushhour{board_size}x{board_size}_{game_number}.csv" # KLOPT DE RELATIVE PATH HIERVAN?
        self.load_cars(board_file)


        # load board
        self.current_board()

        # set winning tile
        win_tile = ceil(self.board_size / 2) * self.board_size
        self.winning_tile = self.tiles[win_tile]

    def load_tiles(self):
        """
            Load tiles
        """

        # add all tiles with occupied to false
        for row in range(1, self.board_size + 1):
            for col in range(1, self.board_size + 1):
                id = ((row - 1) * self.board_size) + col
                new_tile = Tile(id, row, col)
                self.tiles[new_tile.id] = new_tile

    def load_cars(self, board_file):
        """
        Load cars from file
        """
        with open(board_file) as f:
            next(f)
            for line in f:
                car_line = line.split(",")
                self.cars[car_line[0]] = Car(*car_line)


        for car in self.cars:
            # print(self.cars)
            self.cars[car].occupies_tiles(self.board_size)
            self.cars[car].occupation(self.tiles)


    def current_board(self):

        for car in self.cars:
            for tile in self.cars[car].tiles:
                self.tile_occupation[tile] = self.cars[car].id

        for tile in self.tiles:
            if tile in self.tile_occupation:
                self.board.append(self.tile_occupation[tile])
            else:
                self.board.append("_")

            if self.tiles[tile].id % self.board_size == 0:
                self.board.append("\n")


    def valid_move(self, car_id, move):
        """
        Checks if the move is valid
        """
        car = self.cars[car_id]
        move = int(move)

        # check if you don't move through any cars or walls, return false if you do
        # if the car's orientation is horizontal, only look through its row 
        if car.orientation == 'H':
            # check if you don't move through walls
            if 1 > car.col + move or car.col + car.length - 1 + move > self.board_size:
                print("muur1")
                return False

            # TODO: ook werkend krijgen voor negatieve bewegingen
            if move < 0:
                for i in range(move, car.row - 1):
                    if self.tiles[((car.row - 1) * self.board_size + car.col) + i].occupied:
                        print("auto1")
                        return False
            # check if you don't move through cars
            for i in range(car.length, move + car.length - 1):
                if self.tiles[((car.row - 1) * self.board_size + car.col) + i].occupied:
                    print("auto2")
                    return False
        # if it is vertical, only look through its column
        else:
            if 1 > car.row + move or car.row + car.length - 1 + move > self.board_size:
                print("muur2")
                return False
        
            if move < 0:
                    for i in range(move, car.col - 1):
                        if self.tiles[((car.row + i - 1) * self.board_size) + car.col].occupied == False:
                            return False
            for i in range(car.length, move + car.length - 1):
                if self.tiles[((car.row + i - 1) * self.board_size) + car.col].occupied == False:
                    return False
        
        return True

    def move(self, car_id, move):
        """
        Move a car to a different possition
        """
        move = int(move)
        # set current tiles to unoccupied
        for tile in self.cars[car_id].tiles:
            self.tiles[tile].set_unoccupied()
            # tile_car = 
            self.board[floor(tile / self.board_size) - 1 + tile] = "_"
            # tile_car.replace(tile_car, "_")

        # set new position car 
        self.cars[car_id].update_position(move, self.board_size)

        # set tiles to occupied 
        for tile in self.cars[car_id].tiles:
            self.tiles[tile].set_occupied()
            self.board[floor(tile / self.board_size) - 1 + tile] = car_id
            print(self.tiles[tile].id, self.tiles[tile].occupied)

        # print(self.board)

    def give_board(self):
        return " ".join(self.board)

    def game_won(self):
        """
        Checks if the red car (with id X) is in front of the exit
        """
        if self.winning_tile in self.cars['X'].tiles:
            return True
        return False