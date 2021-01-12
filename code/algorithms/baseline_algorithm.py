from code.classes.car import Car

from random import choice

class Baseline():

    def __init__(self, board_size, game_number):
        self.board_size = board_size
        self.game_number = game_number
        self.cars = {}
        self.board_file = f"data/gameboards/Rushhour{board_size}x{board_size}_{game_number}.csv"

        self.load_cars(self.board_file)


    def load_cars(self, board_file):
        with open(board_file) as f:
            next(f)
            for line in f:
                car_line = line.split(",")
                self.cars[car_line[0]] = Car(*car_line)


    def get_command(self):
        # pick random car
        car = choice(list(self.cars.values()))
        print(car)

baseline = Baseline(6,1)
baseline.get_command()



