from copy import deepcopy
from random import choice


from code.classes.game import Game


class Random_repeater():
    
    def __init__(self, board_size, game_number):
        self.board_size = int(board_size)
        self.game_number = game_number
        self.board_file = f"data/gameboards/Rushhour{board_size}x{board_size}_{game_number}.csv" # DIT KAN DENK IK WEG
        

        # self.cars = []
        # self.load_cars(self.board_file)
        
        self.best_solution = [] # deze kunnen we ook nog verbeteren met heen en weer moves weghalen
        self.best_game = None

        for i in range(100):
            self.game = Game(self.board_size, self.game_number)
            new_solution = self.create_solution()
            if new_solution:
                print(len(new_solution))
                self.best_solution = new_solution
                self.best_game = self.game
            if i % 1000 == 0:
                print(f"We are at {i} tries!")

        # print(self.best_solution)


    def create_solution(self):
        solution = []

        while True:

            car = choice(list(self.game.car_ids))
            while True:
                move = choice(range(-(self.board_size - 2), self.board_size - 1)) # VOLGENS MIJ MOET DIT BOARD_SIZE - 2 ZIJN IPV + 2
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

    def get_game(self):
        return self.best_game

    def get_command(self):
        command_list = self.best_solution.pop(0)
        car, move = command_list[0:2]
        return f"{car},{move}"