from .breadth_first import BreadthFirst
from code.classes.game import Game

import copy


class DepthFirst(BreadthFirst):
    def get_next_state(self):
        key = self.state_keys.pop()
        
        print(f"Queue length: {len(self.state_keys)}")
        
        return self.states[key]

    def build_children(self, state_data):
        """
        Creates all possible child-states and adds them to the list of states
        """
        game_node = Game(self.game.board_size, self.game.game_number, state_data)
        # print(game_node.give_board())
        # print(game_node.get_moves())

        # 
        for car in game_node.car_ids: 
            for i in range(- game_node.board_size - 2, game_node.board_size - 1):
                if i != 0:
                    # check if the move is valid/possible
                    if game_node.valid_move(car, i):
                        if game_node.get_moves() and [car,-i] == game_node.get_moves()[-1]:
                            break
                        # make a new state
                        new_game_state = Game(self.game.board_size, self.game.game_number, copy.deepcopy(state_data))
                        # new_game_state = copy.deepcopy(game_node)
                        # move the car
                        new_game_state.move(car, i)
                        # print(f"Na Move: {new_game_state.get_moves()}")

                        # check if it is a solution
                        if new_game_state.game_won():
                            self.best_solution = new_game_state.get_moves()
                            # print(self.best_solution)
                            print(len(self.best_solution))
                        else:
                            if len(new_game_state.get_moves()) < 30:
                                self.queue += 1
                                print(f"Added to queue: {self.queue}")
                                print(f"Depth: {len(new_game_state.get_moves())}")
                                self.state_keys.append(new_game_state.give_board())
                                self.states[new_game_state.give_board()] = self.get_car_coords(new_game_state)