from copy import deepcopy
from random import choice

from .random_repeater import Random_repeater
from code.classes.game import Game

class AStar:
    """
    Implements an attempt at A* with questionable heuristics.
    """

    def __init__(self, game):

        # create solution with random repeater
        self.solution = Random_repeater(board_size, game_number).get_game()
        self.max_moves = len(self.solution.get_moves())
        self.game = deepcopy(game)

        # archive
        self.states = {}
        self.add_to_archive(self.game)

        # game properties
        self.move_range = self.game.get_move_range()
        self.cars = self.game.get_cars()
        self.best_solution = None

        # calculate score of starting board
        self.score = self.calculate_score(self.game)

        self.shorten_solution()


    def calculate_score(self, game):
        """
        Calculate board score based on difference between current board and 
        the winning state from random repeater.
        """
        # start with amount of moves performed
        score = len(game.get_moves())

        # compare current car location to location in winning state
        for car in self.solution.cars:
            # retrieve car info for both states
            solution_info = self.solution.cars[car].car_attributes()
            game_info = game.cars[car].car_attributes()

            # weigh car X more heavily
            if car == "X":
                score += 4 * abs(solution_info["col"] - game_info["col"])
            elif self.solution.cars[car].orientation == "H":
                score += abs(solution_info["col"] - game_info["col"])
            else:
                score += abs(solution_info["row"] - game_info["row"])
        
        return score
    

    def check_length(self):
        """
        Check whether more moves have been performed than in the random solution. 
        If too long, perform loop cutter and continue searching.
        """
        if len(self.game.get_moves()) >= self.max_moves:

            # perform loop cutter, create new game and perform remaining moves
            new_moves = self.remove_loops(self.game.get_moves())
            self.game = Game(self.solution.game_size, self.solution.game_number)
            for move in new_moves:
                self.game.move(*move)
            
            # perform random moves for every restart
            for i in range(self.restart):
                while True:
                    car = choice(self.cars)
                    move = choice(self.move_range)
                    if self.game.valid_move(car, move):
                        self.game.move(car, move)
                        break


    def shorten_solution(self):
        """
        Tries to find shorter solution 
        """
        while True:
            best_score = float('inf')
            ni_score = float('inf')
            best_move = None
            valid_moves = 0

            # iterate through all moves and check if maximum length has been exceeded
            for car in self.cars: 
                for i in self.move_range:
                    self.check_length()
                    
                    # check if the move is valid/possible
                    if self.game.valid_move(car, i):
                        valid_moves += 1

                        # if previous move performed with this car, skip it
                        if self.game.get_moves() and car == self.game.get_moves()[-1][0]:
                            continue
                        
                        # make new game and check if move improves score
                        new_board = Game(self.solution.game_size, self.solution.game_number, deepcopy(self.get_node_data(self.game)))
                        new_board.move(car, i)
                        new_score = self.calculate_score(new_board)
                        
                        # save move if it improves score
                        if new_score < best_score and new_board.give_board() not in self.states:
                            print(new_score, best_score)
                            best_score = new_score
                            best_move = [car, i]
                        # save move with lowest score from this round    
                        elif new_score < ni_score and new_board.give_board() in self.states:
                            ni_score = new_score
                            ni_move = [car, i]

            # perform best move          
            if best_move:
                self.game.move(*best_move)
                self.add_to_archive(self.game)

                if new_board.game_won():
                    self.best_solution = self.game.get_moves()
                
                if self.best_solution != None:
                    break
            # go back to previous board if it is the only move possible
            elif valid_moves == 1:
                back_track = self.game.get_moves(self.game)[-1]
                self.game.move(*back_track)
                print("backtracked")
            # perform non-ideal move with lowest score
            else:
                self.game.move(*ni_move)

            
    def remove_loops(self, moves):
        """
        Checks for double board configurations in current moves.
        If found, removes all moves in between.
        """
        # recreate current game and perform all moves while saving board configurations
        game = Game(self.solution.game_size, self.solution.game_number)
        game_boards = []
        game_boards.append(game.give_board())

        for move in moves:
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
                    print(f"Removed move {board_indices[0]} to {board_indices[-1]}")
                    del moves[board_indices[0]: board_indices[-1]]

                    break
            else:
                break

        return moves


    def add_to_archive(self, game):
        """
        Creates archive of previously encountered board configurations.
        """
        if game.give_board() not in self.states:
            self.states[game.give_board()] = self.get_node_data(game)


    def get_node_data(self, game_node):
        """
        Make list with car, orientation, column, row and length and moves
        """
        info = []
        for car_id in game_node.cars:
            car = game_node.cars[car_id]
            info.append(f"{car.id},{car.orientation},{car.col},{car.row},{car.length}")
        moves = game_node.get_moves()

        return [info, moves]

    
    def get_command(self):
        """
        One by one, return moves from obtained solution to main.
        """
        command_list = self.best_solution.pop(0)
        car, move = command_list[0:2]

        return f"{car},{move}"
