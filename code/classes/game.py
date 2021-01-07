from tile import Tile
from car import Car

class Game:
    def __init__(self, dimension, board_file):

        self.dimension = dimension

        # TODO: inladen auto's en tiles
        self.tiles = {}
        self.cars = {}

        self.load_tiles(dimension)
        self.load_cars(board_file)

    def load_cars(self, board_file, dimension):
        """
        Load cars from file
        """
        with open(board_file) as f:
            for line in f:
                car_line = f.readline().split(",")
                self.cars[car_line[0]] = Car(*car_line)

    def load_tiles(self, dimension):
        """
        Load tiles
        """
        pass

    def current_board(self):
        pass

    # TODO: aanpassen
    def valid_move(self, car, destination):
        """
        Checks if the car is moved within it's row or column
        """
        # if the orenientation of the car is horizontal, check if the move is in the same row
        if car.orientation == 'H':
            return 
        # if the orientation is vertical, check if the move is in the same column
        elif car.orientation == 'V':
        
        # check of beweging mogelijk is (hij gaat niet door andere auto's of muren heen)
        # return false als dat wel zo is 
        Voor elke tegel die gepasseerd wordt:
            als de tegel occupied is:
                return False
        als destination of destination+1 niet op bord:
            return false


    def move(self, car, destination):
        """
        Move a car to a different possition, if possible
        """

        # if the move is valid, change the position of the car
        # set current tiles to unoccupied
        for tile in self.cars[car.id].tiles:
            tile.set_unoccupied()

        # set new position car 
        # TODO: method uit Car class
        self.cars[car.id].row = destination.row
        self.cars[car.id].col = destination.col

        # set tiles to occupied 
        for tile in self.cars[car.id].tiles:
            tile.set_occupied()
        
        return True

    def game_won(self):
        """
        Checks if the red car (with id X) is in front of the exit
        """
        als auto X op row == dimension-1 & col = dim/2(even) of col= dim/2+1(oneven) staat
            return True
        return False  
