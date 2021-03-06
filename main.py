"""
This file is used to run a Rushhour game. It loads the correct game file and solves
it using the algorithm specified by the user. 
"""

# importing all algorithms
from code.algorithms.random import Random
from code.algorithms.random_repeater import Random_repeater
from code.algorithms.iterative_depth_first import Iterative_depth_first
from code.algorithms.breadth_first import Breadth_first
from code.algorithms.depth_first import Depth_first
from code.algorithms.random_loopcutter import Random_loopcutter
from code.algorithms.astar import AStar
from code.algorithms.breadthfirst_improver import Breadthfirst_improver

from code.classes.game import Game
from code.advanced.generate_board import GenerateBoard

import csv
import os
from sys import argv


if __name__ == "__main__":
    print("Do you want to generate a random new board?")
    answer = input("> ")
    
    # generate a new gameboard
    if answer == 'yes' or answer == 'y':
        # ask user for board size
        while True:    
            print("What size board do you want?") 
            board_size = input("> ")
            if int(board_size) in [6, 9, 12]:
                break
            print("Invalid board size. Board size can be either 6, 9 or 12")

        # get game number
        for root, dirs, files in os.walk("data/gameboards"):
            game_number = len(files) + 1
            print(f"Game number: {game_number}")
        
        # generate a new gameboard file
        GenerateBoard(board_size, game_number)
    
        # load game
        game = Game(board_size, game_number)
    # load existing gameboard
    else:
        # get board size
        while True:    
            print("What size board do you want?") 
            board_size = input("> ")
            if int(board_size) in [6, 9, 12]:
                break
            print("Invalid board size. Board size can be either 6, 9 or 12")
        
        # get game number
        print("What game do you want to play?")
        game_number = input("> ")

        # load game
        try:
            game = Game(board_size, game_number)
        except:
            print("That game does not exist")
            exit(1)
    
    # ask user what algorithm they want to run
    print("Type the number of the algorithm that you want to run")
    print("1 random: find a solution by performing random moves")
    print("2 breadth first recursive: breadth first without heuristics")
    print("3 breadth first: breadth first with dictionary heuristic")
    print("4 depth first: finds the first solution using depth first")
    print("5 random repeater: tries to fill in random moves to win the game repeatedly")
    print("6 random loopcutter: removes loops from random solution")
    print("7 A*: random combined with A*")
    print("8 breadthfirst improver: improves an existing solution with breadthfirst")

    # keep asking for input until an algorithm is loaded
    while True:
        algorithm_number = input("> ")

        # make sure an integer value is given
        try:
            algorithm_number = int(algorithm_number)
        except:
            print("Invalid algorithm number")
            continue

        # load requested algorithm
        if algorithm_number == 1:
            algorithm = Random(game)
        elif algorithm_number == 2:
            algorithm = Iterative_depth_first(game)
        elif algorithm_number == 3:
            algorithm = Breadth_first(game)
        elif algorithm_number == 4:
            algorithm = Depth_first(game)
        elif algorithm_number == 5:
            # ask the user how many times it should be repeated
            print("How many times do you want to repeat the random algorithm?")
            repeated = input("> ")
            algorithm = Random_repeater(game, repeated)
        elif algorithm_number == 6:
            algorithm = Random_loopcutter(game)
        elif algorithm_number == 7:
            algorithm = AStar(game)
        elif algorithm_number == 8:
            # get the max depth and the file location of the solution
            print("What depth do you want to use for the breadth first improver?")
            max_depth = input("> ")
            print("What is the relative file location of the solution you want to improve?")
            print("Example: data/output_files/output.csv")
            solution_file = input("> ")
            algorithm = Breadthfirst_improver(game, max_depth, solution_file)
        else:
            print("Invalid algorithm number")
            continue

        break

    # initiate move registration and move counters
    command_list = ""
    command_count = 0

    # initiate output file
    with open('data/output_files/output.csv', 'w', newline ='') as outputfile:
        writer = csv.writer(outputfile)
        writer.writerow(["car", "move"])

    print(" " + game.give_board())
    
    # ask algorithm for input
    while True:
        command_string = algorithm.get_command()
        command_count += 1
        
        # update output string and perform move
        command_list += f"{command_string}\n"
        command = command_string.split(",")
        game.move(*command)

        # exit when game is won
        if game.game_won():
            # print final gameboard state and total number of moves
            print(" "+game.give_board())
            print(command_count)
            print("Congratulations, you have won the game!")

            # write all valid moves to output file
            with open('data/output_files/output.csv', 'a') as outputfile:
                outputfile.write(command_list)

            exit(0)
        
