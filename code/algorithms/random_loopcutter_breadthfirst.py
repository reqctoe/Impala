from copy import deepcopy
from random import choice # kijken of dit weg kan

from code.classes.game import Game
from code.algorithms.random_repeater import Random_repeater


class Random_repeater_adjusted(Random_repeater):

    def __init__(self, board_size, game_number):
        self.board_size = int(board_size)
        self.game_number = game_number
        self.board_file = f"data/gameboards/Rushhour{board_size}x{board_size}_{game_number}.csv"
        
        self.best_solution = []
        self.best_solutions = []

        for i in range(10000):
            self.game = Game(self.board_size, self.game_number)
            new_solution = self.create_solution()
            if new_solution:
                print(len(new_solution))
                self.best_solution = new_solution
                self.best_solutions.append(new_solution)

    def give_solutions(self):
        return self.best_solutions




class Random_loopcutter_breadthfirst:
    def __init__(self, game):
        self.game = deepcopy(game)

        # select the 10 best solutions out of 1000 tries
        self.random_repeater = Random_repeater_adjusted(self.game.board_size, self.game.game_number)
        self.solutions = self.random_repeater.give_solutions()
        self.solutions = self.solutions[-11:-1]
        self.cut_solutions = []

        for solution in self.solutions:
            self.cut_solutions.append(self.loopcutter(solution))

    def loopcutter(self, solution):
        game = deepcopy(self.game)
        game_boards = []
        game_boards.append(game.give_board())

        for move in solution:
            game.move()