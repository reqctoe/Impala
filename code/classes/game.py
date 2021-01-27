from .tile import Tile
from .car import Car

from math import ceil, floor

class Game():
    """
    This class implements a game of Rush Hour with predetermined board size.
    It can create tile and car objects with winning condition. 
    Moves can be checked for validity and then performed.   
    """
    
    def __init__(self, board_size, game_number, data = None):
        
        # game constants
        self.board_size = int(board_size)
        self.game_number = int(game_number)
        self.winning_tile = ceil(self.board_size / 2) * self.board_size
       
        # board occupation list
        self.board = []
        
        # map tile numbers to occupying car
        self.tiles = {}
        self.tile_occupation = {}
        self.cars = {}
        self.car_ids = []
        
        self.load_tiles()
        
        # load cars and tiles from board file or provided data
        if not data:
            self.data = data
            self.moves = []
            board_file = f"data/gameboards/Rushhour{self.board_size}x{self.board_size}_{self.game_number}.csv" 
        else:
            self.data = data[0]
            self.moves = data[1]
            board_file = self.data
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
        Load cars from provided data or csv file
        """
        # provided data
        if self.data:
            for line in board_file:
                car_line = line.split(",")
                self.cars[car_line[0]] = Car(*car_line)
        # csv file
        else:    
            with open(board_file) as f:
                next(f)
                for line in f:
                    car_line = line.split(",")
                    self.cars[car_line[0]] = Car(*car_line)

        # create tile occupancy dictionary and car ID list 
        for car in self.cars:
            self.cars[car].occupies_tiles(self.board_size)
            self.car_ids.append(self.cars[car].car_attributes()["id"])
            
            # set tile objects to occupied
            for tile in self.cars[car].tiles:
                self.tiles[tile].set_occupied()


    def current_board(self):
        """
        Create board configuration string
        """
        
        # check for occupation and create dictionary of occupied tiles
        for car in self.cars:
            # load car attributes
            car_info = self.cars[car].car_attributes()
            
            for tile in car_info["tiles"]:
                if len(car_info["id"]) == 2:
                    self.tile_occupation[tile] = car_info["id"] + " "
                else:
                    self.tile_occupation[tile] = car_info["id"] + "  "

        for tile in self.tiles:
            # check if tile in occupation dictionary
            if tile in self.tile_occupation:
                self.board.append(self.tile_occupation[tile])
            else:
                self.board.append("_  ")

            # load tile attributes and add newlines 
            tile_info = self.tiles[tile].tile_attributes()
            if tile_info["id"] % self.board_size == 0:
                self.board.append("\n\n")


    def valid_move(self, car_id, move):
        """
        Checks if the move is valid
        """
        
        car = self.cars[car_id].car_attributes()
        move = int(move)
        comp = (car["row"] - 1) * self.board_size

        # check move validity for horizontal car
        if car["orientation"] == "H":
            # left wall
            if car["col"] + move < 1:
                return False
            # right wall
            elif car["col"] + car["length"] - 1 + move > self.board_size:
                return False

            # car left
            if move == -1:
                if self.tiles[car["col"] - 1 + comp].get_occupied():
                    return False
            else:
                for tile in range(car["col"] + move + comp, car["col"] + comp):
                    if self.tiles[tile].get_occupied():
                        return False
           
            # car right
            if move == 1:
                if self.tiles[car["col"] + car["length"] + comp].get_occupied():
                    return False
            else:
                for tile in range(car["col"] + car["length"] + comp, car["col"] + car["length"] + move + comp):
                    if self.tiles[tile].get_occupied():
                        return False

        # check move validity for vertical car      
        else:
            # top wall
            if car["row"] + move < 1:
                return False
            # bottom wall
            elif car["row"] + car["length"] - 1 + move > self.board_size:
                return False
            
            # car top
            if move == -1:
                if self.tiles[car["col"] + comp - self.board_size].get_occupied():
                    return False
            else:
                for tile in range(car["col"] + comp + move * self.board_size, car["col"] + comp, self.board_size):
                    if self.tiles[tile].get_occupied():
                        return False
            
            # car bottom
            if move == 1:
                if self.tiles[car["col"] + comp + car["length"] * self.board_size].get_occupied():
                    return False
            else:
                for tile in range(car["col"] + comp + car["length"] * self.board_size, car["col"] + comp + (car["length"] + move) * self.board_size, self.board_size):
                    if self.tiles[tile].get_occupied():
                        return False

        return True


    def move(self, car_id, move):
        """
        Move a car to a different position
        """
        
        move = int(move)
        car_info = self.cars[car_id].car_attributes()

        self.moves.append([car_id,move])

        # set current tiles to unoccupied and update board string
        for tile in car_info["tiles"]:
            self.tiles[tile].set_unoccupied()
            self.board[floor((tile - 1) / self.board_size) - 1 + tile] = "_  "

        # set new position car 
        self.cars[car_id].update_position(move, self.board_size)

        # set tiles to occupied  and update board string
        for tile in car_info["tiles"]:
            self.tiles[tile].set_occupied()

            if len(car_id) == 2:
                self.board[floor((tile - 1)/ self.board_size) - 1 + tile] = car_id + " "
            else:
                self.board[floor((tile - 1)/ self.board_size) - 1 + tile] = car_id + "  "
    

    def get_game_info(self):
        """
        Create dictionary of board size and game number
        """
        return {
            "board_size": self.board_size, 
            "game_number": self.game_number
        }


    def get_cars(self):
        """
        Make list of car ID's
        """
        return self.car_ids


    def get_moves(self):
        """
        Give moves performed in game object
        """
        return self.moves


    def get_move_range(self):
        """
        Give move range inherent to board
        """
        move_range = list(range(- self.board_size + 2, self.board_size - 1))
        move_range.remove(0)
        
        return move_range


    def give_board(self):
        """
        Creates and returns board configuration string
        """
        return " ".join(self.board)


    def game_won(self):
        """
        Checks if the red car (with id X) is in front of the exit
        """
        
        if self.winning_tile in self.cars['X'].car_attributes()["tiles"]:
            return True
        return False
