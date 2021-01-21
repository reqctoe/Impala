from copy import deepcopy
from random import choice # kijken of dit weg kan

from code.classes.game import Game
from code.algorithms.random_repeater import Random_repeater


class Random_repeater_adjusted(Random_repeater):

    def give_solution(self):
        return self.best_solution


class Random_loopcutter_breadthfirst:
    def __init__(self, game):
        self.game = deepcopy(game)

        # get best solutions out of 1000 random tries using Random_repeater
        self.random_repeater = Random_repeater_adjusted(self.game.board_size, self.game.game_number)
        self.solution = self.random_repeater.give_solution()

        # cut loops of every solution an keep save shortest result
        self.cut_solution = self.loopcutter(self.solution)

    def loopcutter(self, solution):
        game = deepcopy(self.game)
        game_boards = []
        game_boards.append(game.give_board())

        for move in solution:
            game.move(*move)
            game_boards.append(game.give_board())

        # keep cutting until there are no more double states left
        while True:
            game_boards_set = set(game_boards)

            for board in game_boards_set:
                # get all indices of a game state in board_list
                board_indices = [i for i, e in enumerate(game_boards) if e == board]

                # if a state occurs more than once, delete the moves in between
                if len(board_indices) > 1:
                    del game_boards[board_indices[0]: board_indices[-1]]
                    del solution[board_indices[0]: board_indices[-1]]
                    print(f"Removed move {board_indices[0]} to {board_indices[-1]}")
                    break
            # when no duplicates are found anymore, stop cutting
            else:
                break

        return solution



    def get_command(self):
        command_list = self.cut_solution.pop(0)
        car, move = command_list[0:2]
        return f"{car},{move}"
