"""
This file is used to run a Rushhour game. It loads the correct game file and solves
it using the algorithm specified by the user. 
"""

# importing all algorithms
from code.algorithms.random import Random
from code.algorithms.random_repeater import Random_repeater
from code.algorithms.test_alg_2 import Test_alg_2
from code.algorithms.breadth_first import BreadthFirst
from code.algorithms.depth_first import DepthFirst
from code.algorithms.random_loopcutter import Random_loopcutter
from code.algorithms.astar import AStar
from code.algorithms.breadthfirst_improver import Breadthfirst_improver
from code.generate_board import GenerateBoard

from code.classes.game import Game

import csv
from sys import argv


if __name__ == "__main__":

    # check if command line arguments are given
    if len(argv) != 3:
        print("Usage: python main.py [game_number] [board_size]")
        exit(1)
    
    # check game number
    # if int(argv[1]) not in range(1, 8):
    #     print("Invalid game number")
    #     exit(1)

    # check board size
    if int(argv[2]) not in [6, 9, 12]:
        print("Invalid board size")
        exit(1)

    # generate a new gameboard
    print("Do you want to generate a random new board?")
    answer = input("> ")

    # if the user wants to generate a new gameboard file, ask for the size and number
    if answer == 'yes' or answer == 'y':
        print("What size board do you want?") 
        board_size = input("> ")
        print("What is the number of the game?")
        game_number = input("> ")

        while True:
            if int(game_number) not in range(1,8):
                break
            print("A game with that number already exists\nPlease enter a new number")
            game_number = input("> ")
        
        # generate a new gameboard file
        GenerateBoard(board_size, game_number)
    
        # load game
        game = Game(board_size, game_number)
        print(game.give_board())
    else:
        # load game
        game_number, board_size = argv[1], argv[2]
        game = Game(board_size, game_number)
    
    # ask user what algorithm they want to run
    print("Type the number of the algorithm that you want to run")
    print("1 random: Fills in random moves")
    print("2 random repeater: tries to fill in random moves to win the game repeatedly")
    print("3 test alg 2: breadth first without heuristics")
    print("4 breadth first: breadth first with dictionary heuristic")
    print("5 depth first: depth first")
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
            algorithm = Random_repeater(game)
        elif algorithm_number == 3:
            algorithm = Test_alg_2(board_size, game_number)
        elif algorithm_number == 4:
            algorithm = BreadthFirst(game)
        elif algorithm_number == 5:
            algorithm = DepthFirst(game)
        elif algorithm_number == 6:
            algorithm = Random_loopcutter(game)
        elif algorithm_number == 7:
            algorithm = AStar(board_size, game_number)
        elif algorithm_number == 8:
            algorithm = Breadthfirst_improver(game)
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
        
