from copy import deepcopy

from code.algorithms.breadth_first import Breadth_first
from code.classes.game import Game

class BreadthFirst_adjusted(Breadth_first):
    """
    This class inherits from the breadthfirst algorithm and contains some
    adjustments to make it suitable to improve an existing solution with
    the Breadthfirst_improver algorithm. Parameters: game(Game object), 
    boards(list of strings), max_depth(int), step_counter(int).
    """

    def __init__(self, game, boards, max_depth, step_counter):
        self.boards = boards
        self.game = deepcopy(game)
        self.max_depth = max_depth
        self.step_counter = step_counter

        # initialise archive
        self.state_keys = []
        self.states = {}
        self.add_to_archive(game)
        
        # game variables
        self.move_range = self.game.get_move_range()
        self.cars = game.get_cars()

        self.index = None
        self.best_solution = None

        self.run_breadth_first()


    def build_child(self, game_node, car, move):
        """
        Performs a move and checks if it results in a board that is present
        further on in the solution. If it is, the solution and the index of 
        the board further on in the solution are saved. 
        Parameters: game_node(Game object), car(string), move(int).
        """
        # make new state and perform move
        new_node = Game(self.game.board_size, self.game.game_number, deepcopy(self.get_node_data(game_node)))
        new_node.move(car, move)
        
        # check if shorter solution has been found
        if [new_node.give_board()] in self.boards:
            # save solution and index
            self.best_solution = new_node.get_moves()
            self.index = self.boards.index([new_node.give_board()])  
        else:
            # if depth is greater then the max depth, stop adding to queue
            if len(new_node.get_moves()) <= (self.max_depth + self.step_counter):
                self.add_to_archive(new_node)

    def give_solution(self):
        return self.best_solution, self.index

class Breadthfirst_improver:
    """
    This class implemants an algorithm that improves an existing solution with
    the breathfirst algorithm. It applies a complete breadthfirst search with a 
    specified maximum depth to each state(game board configuration) in the 
    initial solution. If it finds a state that is further away than the maximum
    depth, a shorter solution has been found and will be returned.
    Parameter: game(Game object), max_depth(int), solution_file(string).
    """

    def __init__(self, game, max_depth, solution_file):
        self.game = deepcopy(game)
        self.max_depth = int(max_depth)
        self.solution_file = solution_file

        # load solution that needs to be improved from file
        self.solution = self.load_solution(self.solution_file)

        # make a list of game states
        self.game_boards, self.game_boards_total_length = self.make_game_states_list(self.game, self.solution, self.max_depth)

        # improve the solution using breadthfirst
        self.run_improver()


    def load_solution(self, solution_file):
        """
        Loads the solution from the file into a list.
        """
        with open(solution_file) as f:
            # skip header
            next(f)
            solution = []

            for line in f:
                move = line[:-1].split(",")
                solution.append(move)
        
        return solution


    def make_game_states_list(self, game, solution, depth):
        """
        Returns the total length of all the game boards found in the initial
        solution and a shorter list of string represenatations of the game 
        boards needed for the first depth first search. Parameters:
        game(Game object), solution(nested list with moves), depth(int).
        """
        
        # initialise game and boards list
        game_for_boards = deepcopy(game)
        game_boards = []
        game_boards.append([game_for_boards.give_board()])

        # add boards to list
        for move in solution:
            game_for_boards.move(*move)
            game_boards.append([game_for_boards.give_board()])

        # save total length and prepare list for first iteration
        game_boards_total_length = len(game_boards)
        game_boards = game_boards[depth + 2:]

        return game_boards, game_boards_total_length


    def run_improver(self):
        """
        Runs breathfirst on each state and returns if a better solution 
        has been found or if all the states have been checked.
        """
        step_counter = 0

        while self.game_boards:
            
            print(f"Checking board {step_counter + 1}")
            print(f"Boards remaining: {len(self.game_boards)}")

            # run breadthfirst
            breadthfirst = BreadthFirst_adjusted(self.game, self.game_boards, self.max_depth, step_counter)
            partial_solution, index = breadthfirst.give_solution()

            if partial_solution:
                # replace that piece of code in the solution
                self.solution[: (self.game_boards_total_length - len(self.game_boards) + index)] = partial_solution
                return

            self.game_boards.pop(0)
            self.game.move(*self.solution[step_counter])
            step_counter += 1


    def get_command(self):
        """
        Returns the command to move a car
        """
        command_list = self.solution.pop(0)
        car, move = command_list[0:2]

        return f"{car},{move}"