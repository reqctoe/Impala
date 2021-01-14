from copy import deepcopy
from random import choice


from code.classes.game import Game


class Test_alg_1():
    
    def __init__(self, board_size, game_number):
        self.board_size = int(board_size)
        self.game_number = game_number
        self.board_file = f"data/gameboards/Rushhour{board_size}x{board_size}_{game_number}.csv"

        self.cars = []
        self.load_cars(self.board_file)
        self.game_standard = Game(board_size, game_number)

        
        self.best_solution = [] # deze kunnen we ook nog verbeteren met heen en weer moves weghalen

        for i in range(10000):
            self.game = deepcopy(self.game_standard)
            new_solution = self.create_solution()
            if new_solution:
                print(len(new_solution))
                self.best_solution = new_solution
            if i % 1000 == 0:
                print(f"We are at {i} tries!")

        print(self.best_solution)


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


    def create_solution(self):
        solution = []

        while True:

            car = choice(list(self.cars))
            while True:
                move = choice(range(-(self.board_size + 2), self.board_size - 1))
                if move != 0:
                    if solution:
                        if [car, -move] != solution[-1]:
                            break
                    else:
                        break             

            if not self.game.valid_move(car, move):
                continue

            self.game.move(car, move)
            solution.append([car,move])

            if self.best_solution and len(solution) >= len(self.best_solution):
                return False

            if self.game.game_won():
                return solution


    def get_command(self):
        command_list = self.best_solution.pop(0)
        car, move = command_list[0:2]
        return f"{car},{move}"