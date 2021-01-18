

from random import choice


class Baseline():
    """
    This class is used to implement a baseline algorithm to solve the
    Rushhour game. Parameters for initialisation: board size(string),
    board number (string).
    """

    def __init__(self, board_size, game_number):
        self.board_size = int(board_size)
        self.game_number = game_number
        self.cars = []
        self.board_file = f"data/gameboards/Rushhour{board_size}x{board_size}_{game_number}.csv"

        self.load_cars(self.board_file)


    def load_cars(self, board_file):
        """
        Loads all the car id's from the board file into a list. 
        Needs the board file name (string) as parameter.
        """

        with open(board_file) as f:
            # skip header and read each car into list
            next(f)

            for line in f:
                car_line = line.split(",")
                self.cars.append(car_line[0])

    def get_command(self):
        """
        Generates a random imput command for the Rushhour game.
        """

        # pick random car and move it one step forward or backward
        car = choice(list(self.cars))
        while True:
            move = choice(range(-(self.board_size + 2), self.board_size - 1))
            if move != 0:
                break
         
        return f"{car},{move}"



