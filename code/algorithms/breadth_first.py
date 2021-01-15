import copy
from code.classes.game import Game

class BreadthFirst:
    
    def __init__(self, game):
        self.game = copy.deepcopy(game)

        # make copy of the current game
        self.states = {self.game.give_board(): self.get_car_coords(self.game)}
        self.state_keys = [self.game.give_board()]

        self.best_solution = None
        self.queue = int(0)

        self.create_solution()



    def get_car_coords(self, game_state):
        """
        Make list with car, orientation, column, row and length and moves
        """
        info = []
        for car_id in game_state.cars:
            car = game_state.cars[car_id]
            info.append(f"{car.id},{car.orientation},{car.col},{car.row},{car.length}")

        moves = game_state.get_moves()
        # print([info, moves])
        return [info, moves]        


    def get_next_state(self):
        # return self.states.pop(0)
        key = self.state_keys.pop(0)
        
        print(f"Queue length: {len(self.state_keys)}")
        
        return self.states[key]

    def build_children(self, state_data):
        """
        Creates all possible child-states and adds them to the list of states
        """
        game_node = Game(self.game.board_size, self.game.game_number, state_data)

        # 
        for car in game_node.car_ids: 
            for i in range(- game_node.board_size - 2, game_node.board_size - 1):
                if i != 0:
                    # check if the move is valid/possible
                    if game_node.valid_move(car, i):
                        if game_node.get_moves() and [car,-i] == game_node.get_moves()[-1]:
                            break
                        # make a new state
                        new_game_state = Game(self.game.board_size, self.game.game_number, state_data)
                        # move the car
                        new_game_state.move(car, i)

                        # check if it is a solution
                        if new_game_state.game_won():
                            self.best_solution = new_game_state.get_moves()
                            # print(self.best_solution)
                            print(len(self.best_solution))
                        else:
                            if new_game_state.give_board() not in self.states:
                                self.queue += 1
                                print(f"Added to queue: {self.queue}")
                                print(f"Depth: {len(new_game_state.get_moves())}")
                                self.state_keys.append(new_game_state.give_board())
                                self.states[new_game_state.give_board()] = self.get_car_coords(new_game_state)

            
                        # if new_game_state.game_won():
                        #     self.best_solution = new_game_state.get_moves()
                        # else:
                        #     if new_game_state.give_board() not in self.states:
                        #         self.state_keys.append(new_game_state.give_board())
                        #         self.states[new_game_state.give_board()] = new_game_state
                            # self.states.append(new_game_state)
    
    def create_solution(self): # moet dit in main.py of in de init worden aangeroepen?
        """
        Zolang je self.states lijst niet leeg is:
            RIJ 1:
                pak de begin state 
            RIJ 2-n:
                pak het eerste element uit state lijst
                check of solution
                nee:
                    gooi in build_children
                .....               
        """
        count = 0

        while self.state_keys:
        # while self.states:
            count += 1
            new_state_data = self.get_next_state()
            if count % 5 == 0:
                print(f"ROW:{len(new_state_data[1])}")

            self.build_children(new_state_data)

            if self.best_solution != None:
                break

    def get_command(self):
        command_list = self.best_solution.pop(0)
        car, move = command_list[0:2]
        return f"{car},{move}"
        
            