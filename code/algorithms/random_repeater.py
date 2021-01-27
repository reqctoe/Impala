from random import choice

from code.classes.game import Game


class Random_repeater():
    """
    This class is used to implement an algorithm that uses random moves to solve the
    Rushhour game. This is repeated n times, stopping as soon as the current solution
    becomes longer than the best solution. Parameters for initialisation: game (Game object).
    """
    
    def __init__(self, game, repeated):
        # game variables
        game_info = game.get_game_info()
        self.board_size = game_info["board_size"]
        self.game_number = game_info["game_number"]
        self.cars = game.get_cars()
        self.move_range = game.get_move_range()

        self.repeated = repeated	
        
        # initialize best solution
        self.best_solution = []
        self.best_game = None

        self.find_best_solution()


    def find_best_solution(self):
        """
        Tries n times to find a solution that is as short as possible
        """
        for i in range(self.repeated):
            self.game = Game(self.board_size, self.game_number)
            # try to generate a shorter solution
            new_solution = self.create_solution()
            
            # if there is a shorter solution, save that as the best solution
            if new_solution:
                print(len(new_solution))
                self.best_solution = new_solution
                self.best_game = self.game
            
            # keep track of how far along you are
            if i % 500 == 0:
                print(f"We are at {i} tries!")


    def create_solution(self):
        """
        Tries to generate a random solution that is shorter than the current best solution.
        """
        solution = []

        while True:
            # pick a random car and move it a random number of steps forward or backward
            car = choice(self.cars)
            while True:
                move = choice(self.move_range)
                # make sure the same car is not moved back immediately
                if solution:
                    if [car, -move] != solution[-1]:
                        break
                else:
                    break
            
            # check if move is valid
            if not self.game.valid_move(car, move):
                continue

            # move the car and add the move to the solution
            self.game.move(car, move)
            solution.append([car,move])

            # if the current solution is longer than the best solution, stop
            if self.best_solution and len(solution) >= len(self.best_solution):
                break

            # return the shorter, winning solution
            if self.game.game_won():
                return solution


    def get_game(self): # NAAR A*
        """
        Returns the game object with the best solution
        """
        return self.best_game


    def get_command(self):
        """
        Returns the command to move a car
        """
        command_list = self.best_solution.pop(0)
        car, move = command_list[0:2]
        return f"{car},{move}"