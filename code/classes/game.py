from .tile import Tile
from .car import Car

from math import ceil, floor

class Game():
    
    def __init__(self, board_size, game_number):
        
        self.board_size = int(board_size)
        # winning tile id        
        self.winning_tile = ceil(self.board_size / 2) * self.board_size
        # board occupation list
        self.board = []
        # map tile numbers to occupying car
        self.tile_occupation = {}
        # map tile numbers to the corresponding tile object
        self.tiles = {}
        # map car letters to the corresponding car object
        self.cars = {}
        self.car_ids = []

        self.moves = []

        # load cars and tiles from board file
        board_file = f"data/gameboards/Rushhour{board_size}x{board_size}_{game_number}.csv" 
        self.load_tiles()
        self.load_cars(board_file)

        # load board
        self.current_board()


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


    def load_cars(self, board_file):
        """
        Load cars from file
        """

        # open file and create car objects
        with open(board_file) as f:
            next(f)
            for line in f:
                car_line = line.split(",")
                self.cars[car_line[0]] = Car(*car_line)

        for car in self.cars:
            # create list of tiles occupied by car
            self.cars[car].occupies_tiles(self.board_size)
            self.car_ids.append(self.cars[car].id)
            
            # set tiles to occupied
            for tile in self.cars[car].tiles:
                self.tiles[tile].set_occupied()
            

    def current_board(self):
        """
        Create board configuration string
        """
        
        # check for occupation and create dictionary of occupied tiles
        for car in self.cars:
            for tile in self.cars[car].tiles:
                if len(self.cars[car].id) == 2:
                    self.tile_occupation[tile] = self.cars[car].id + " "
                else:
                    self.tile_occupation[tile] = self.cars[car].id + "  "

        for tile in self.tiles:
            # check if tile in occupation dictionary
            if tile in self.tile_occupation:
                self.board.append(self.tile_occupation[tile])
            else:
                self.board.append("_  ")

            # add newlines 
            if self.tiles[tile].id % self.board_size == 0:
                self.board.append("\n\n")


    def valid_move(self, car_id, move):
        """
        Checks if the move is valid
        """
        
        car = self.cars[car_id]
        move = int(move)
        comp = (car.row - 1) * self.board_size

        # check move validity for horizontal car
        if car.orientation == "H":
            # left wall
            if car.col + move < 1:
                return False
            # right wall
            elif car.col + car.length - 1 + move > self.board_size:
                return False

            # car left
            if move == -1:
                if self.tiles[car.col - 1 + comp].occupied:
                    return False
            else:
                for tile in range(car.col + move + comp, car.col + comp):
                    if self.tiles[tile].occupied:
                        return False
           
            # car right
            if move == 1:
                if self.tiles[car.col + car.length + comp].occupied:
                    return False
            else:
                for tile in range(car.col + car.length + comp, car.col + car.length + move + comp):
                    if self.tiles[tile].occupied:
                        return False

        # check move validity for vertical car      
        else:
            # top wall
            if car.row + move < 1:
                return False
            # bottom wall
            elif car.row + car.length - 1 + move > self.board_size:
                return False
            
            # car top
            if move == -1:
                if self.tiles[car.col + comp - self.board_size].occupied:
                    return False
            else:
                for tile in range(car.col + comp + move * self.board_size, car.col + comp, self.board_size):
                    if self.tiles[tile].occupied:
                        return False
            
            # car bottom
            if move == 1:
                if self.tiles[car.col + comp + car.length * self.board_size].occupied:
                    return False
            else:
                for tile in range(car.col + comp + car.length * self.board_size, car.col + comp + (car.length + move) * self.board_size, self.board_size):
                    if self.tiles[tile].occupied:
                        return False

        return True


    def move(self, car_id, move):
        """
        Move a car to a different possition
        """
        
        move = int(move)

        self.moves.append([car_id,move])

        # set current tiles to unoccupied
        for tile in self.cars[car_id].tiles:
            self.tiles[tile].set_unoccupied()
            self.board[floor((tile - 1) / self.board_size) - 1 + tile] = "_  "

        # set new position car 
        self.cars[car_id].update_position(move, self.board_size)

        # set tiles to occupied 
        for tile in self.cars[car_id].tiles:
            self.tiles[tile].set_occupied()

            if len(car_id) == 2:
                self.board[floor((tile - 1)/ self.board_size) - 1 + tile] = car_id + " "
            else:
                self.board[floor((tile - 1)/ self.board_size) - 1 + tile] = car_id + "  "


    # vgm is er al iets anders dat deze informatie geeft, even zoeken
    def get_moves(self):
        return self.moves

    def give_board(self):
        """
        Creates and returns board configuration string
        """
        
        return " ".join(self.board)


    def game_won(self):
        """
        Checks if the red car (with id X) is in front of the exit
        """
        
        if self.winning_tile in self.cars['X'].tiles:
            return True
        return False