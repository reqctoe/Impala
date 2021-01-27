from copy import deepcopy

from code.algorithms.random_repeater import Random_repeater


class Random_repeater_adjusted(Random_repeater):
    """
    Adjusted version of Random_repeater that also returns the best solution and
    not just commands
    """

    def get_solution(self):
        """
        Returns the best solution found with Random_repeater
        """
        return self.best_solution


class Random_loopcutter():
    """
    This class is used to implement an algorithm to solve the Rushhour game that 
    is an improvement of Random_repeater. It uses the best solution from Random_repeater
    and cuts out the moves between two states that are the same. Parameters for initialisation: 
    game (Game object).
    """

    def __init__(self, game):
        self.game = deepcopy(game)

        # get solution to start with using Random_repeater
        self.random_repeater = Random_repeater_adjusted(self.game, 1000)
        self.solution = self.random_repeater.get_solution()

        # cut loops
        self.cut_solution = self.loopcutter(self.solution)


    def loopcutter(self, solution):
        """
        Cuts out all the moves between two states that are the same
        """
        game = deepcopy(self.game)
        game_boards = []
        game_boards.append(game.give_board())

        # add all states/board configurations to game_boards
        for move in solution:
            game.move(*move)
            game_boards.append(game.give_board())

        # keep cutting until there are no more double states left
        while True:
            game_boards_set = set(game_boards)

            for board in game_boards_set:
                # get all indices of a certain game state in game_boards_set
                board_indices = [i for i, e in enumerate(game_boards) if e == board]

                # if a state occurs more than once, delete the moves in between
                if len(board_indices) > 1:
                    del game_boards[board_indices[0]: board_indices[-1]]
                    del solution[board_indices[0]: board_indices[-1]]

                    print(f"Removed move {board_indices[0]} to {board_indices[-1]}")
                    break
            # when all unique states are checked and no duplicates are found anymore, stop cutting
            else:
                break

        return solution


    def get_command(self):
        """
        Returns the command to move a car
        """
        command_list = self.cut_solution.pop(0)
        car, move = command_list[0:2]
        return f"{car},{move}"
