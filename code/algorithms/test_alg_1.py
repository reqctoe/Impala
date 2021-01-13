from random import choice

from code.classes.game import Game


class Test_alg_1():
    
    def __init__(self, board_size, game_number):
        self.board_size = int(board_size)
        self.game_number = game_number
        self.board_file = f"data/gameboards/Rushhour{board_size}x{board_size}_{game_number}.csv"

        self.cars = []
        self.load_cars(self.board_file)
        self.game = Game(board_size, game_number)
        
        self.best_solution = [] # deze kunnen we ook nog verbeteren met heen en weer moves weghalen

        for _ in range(100):
            new_solution = self.create_solution()

            if new_solution:
                self.best_solution = new_solution


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
            move = choice([-1,1])

            if not self.game.valid_move(car, move):
                continue

            self.game.move(car, move)
            solution.append([car,move])

            if len(solution) > len(self.best_solution):
                return False

            if self.game.game_won():
                return solution


    def get_command(self):
        command_list = self.best_solution.pop(0)
        car, move = command_list[0], command_list[1] # dit kan misschien nog beter opgeschreven
        return f"{car},{move}"