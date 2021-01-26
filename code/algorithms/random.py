from random import choice
from copy import deepcopy


class Random():
    """
    This class is used to implement a baseline algorithm to solve the
    Rushhour game. Parameters for initialisation: game (Game object).
    """

    def __init__(self, game):
        # game variables
        self.game = deepcopy(game)
        self.board_size = game.board_size
        self.cars = game.get_cars()
        self.move_range = game.get_move_range()


    def get_command(self):
        """
        Generates a random imput command for the Rushhour game.
        """
        while True:
            # pick a random car and move it a random number of steps forward or backward
            car = choice(self.cars)
            move = choice(self.move_range)
            
            # if the move is valid, return it
            if self.game.valid_move(car,move):
                self.game.move(car, move)
                return f"{car},{move}"