from copy import deepcopy
from random import choice

from .random_repeater import Random_repeater
from code.classes.game import Game

class AStar:
    def __init__(self, board_size, game_number):
        # self.board_size = 
        self.solution = Random_repeater(board_size, game_number).get_game()
        self.max_moves = len(self.solution.get_moves())
        print(self.solution.give_board())
        print("repeater finished")
        self.board = Game(board_size, game_number)

        # initiate archive
        self.states = {}
        self.add_to_archive(self.board)

        self.move_range = list(range(- self.board.board_size + 2, self.board.board_size - 1))
        self.move_range.remove(0)
        self.cars = [x for x in self.board.car_ids]

        self.best_solution = None

        self.score = self.calculate_score(self.board)
        print(self.score)

        self.restart = 0

        self.shorten_solution()


    def calculate_score(self, game):
        score = len(game.get_moves())

        for car in self.solution.cars:
            if car == "X":
                score += 4 * abs(self.solution.cars[car].col - game.cars[car].col)
            elif self.solution.cars[car].orientation == "H":
                score += abs(self.solution.cars[car].col - game.cars[car].col)
            else:
                score += abs(self.solution.cars[car].row - game.cars[car].row)
            
            # if game.give_board() in self.states:
            #     score += 10

        # print(score)
        return score
    
    def check_length(self):
        if len(self.board.get_moves()) >= self.max_moves:
            self.restart += 1
            print(self.restart)
            # print("loops verwijderen")
            new_moves = self.remove_loops(self.board.get_moves())
            self.board = Game(self.solution.board_size, self.solution.game_number)
            for move in new_moves:
                self.board.move(*move)
            
            for i in range(self.restart):
                while True:
                    car = choice(self.cars)
                    move = choice(self.move_range)
                    if self.board.valid_move(car, move):
                        self.board.move(car, move)
                        break


    def shorten_solution(self):
        # restart = 0
        while True:
            best_score = float('inf')
            ni_score = float('inf')
            best_move = None
            valid_moves = 0


            # already_tried = False
            
            for car in self.cars: 
                for i in self.move_range:
                    self.check_length()
                    # check if the move is valid/possible
                    if self.board.valid_move(car, i):
                        valid_moves += 1
                        if self.board.get_moves() and [car,-i] == self.board.get_moves()[-1]:
                            continue
                        new_board = Game(self.solution.board_size, self.solution.game_number, deepcopy(self.get_node_data(self.board)))
                        new_board.move(car, i)
                        # if new_board.give_board() in self.states:
                        #    continue
                        new_score = self.calculate_score(new_board)
                        
                        if new_score < best_score and new_board.give_board() not in self.states:
                            print(new_score, best_score)
                            best_score = new_score
                            best_move = [car, i]    
                        elif new_score < ni_score and new_board.give_board() in self.states:
                            # print("new repeat move found")
                            ni_score = new_score
                            ni_move = [car, i]
                            
            if best_move:
                # self.score = best_score
                self.board.move(*best_move)
                self.add_to_archive(self.board)
                # print(self.board.get_moves())
                # print(self.board.give_board())
                # input()

                if new_board.game_won():
                    self.best_solution = self.board.get_moves()
                    # print(len(self.best_solution))
                    # print(self.best_solution)
                
                if self.best_solution != None:
                    break
            elif valid_moves == 1:
                back_track = self.get_moves(self.board)[-1]
                self.board.move(*back_track)
                print("backtracked")
            else:
                self.board.move(*ni_move)

            

    def remove_loops(self, moves):
        game = Game(self.solution.board_size, self.solution.game_number)
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
        print(self.max_moves, self.restart)
        command_list = self.best_solution.pop(0)
        car, move = command_list[0:2]
        return f"{car},{move}"
