from code.algorithms.baseline_algorithm import Baseline
from code.algorithms.random_repeater import Random_repeater
from code.algorithms.test_alg_2 import Test_alg_2
from code.algorithms.breadth_first import BreadthFirst
from code.algorithms.depth_first import DepthFirst
from code.algorithms.random_loopcutter_breadthfirst import Random_loopcutter_breadthfirst
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
    if int(argv[1]) not in range(1, 8):
        print("Invalid game number")
        exit(1)

    # check board size
    if int(argv[2]) not in [6, 9, 12]:
        print("Invalid board size")
        exit(1)

    # OM NIEUW BORD TE GENEREREN, NOG BESPREKEN HOE WE DIT WILLEN DOEN
    # print("Do you want to generate a random new board?")
    # answer = input("> ")
    # print("What size board do you want?")
    # board_size = input("> ")
    # print("What is the number of the game?")
    # game_number = input("> ")

    # # generate a new gameboard file if the user want to generate a random new board
    # if answer == 'yes' or answer == 'y':
    #     GenerateBoard(board_size, game_number)
    
    # game = Game(board_size, game_number)
    
    # load game
    game_number, board_size = argv[1], argv[2]
    game = Game(board_size, game_number)

    # # load algorithm
    # algorithm = BreadthFirst(game)
    
    # ask user what algorithm they want to run
    print("Type the number of the algorithm that you want to run")
    print("1 baseline: Fills in random numbers")
    print("2 test alg 1: tries to fill in random numbers and r")
    print("3 test alg 2: breadth first without heuristics")
    print("4 breadth first: breadth first with dictionary heuristic")
    print("5 depth first: depth first")
    print("6 random loopcutter breathfirst: combination of these three algorithms")
    print("7 a star: random combined with a star")
    print("8 breadthfirst improver: improves an existing output with breadthfirst")


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
            algorithm = Baseline(board_size, game_number)
        elif algorithm_number == 2:
            algorithm = Random_repeater(board_size, game_number)
        elif algorithm_number == 3:
            algorithm = Test_alg_2(board_size, game_number)
        elif algorithm_number == 4:
            algorithm = BreadthFirst(game)
        elif algorithm_number == 5:
            algorithm = DepthFirst(game)
        elif algorithm_number == 6:
            algorithm = Random_loopcutter_breadthfirst(game)
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
    
    """
    deze doet nu nog allemaal checks die niet nodig zijn aangezien hij 
    alleen solutions aangereikt krijgt 
    """

    # ask algorithm for input
    while True:
        command_string = algorithm.get_command()
        command_count += 1
        
        # check if move is valid
        command = command_string.split(",")
        
        if not game.valid_move(*command):
            continue
        
        # update output string and perform move
        command_list += f"{command_string}\n"
        # print(game.give_board())
        game.move(*command)


       
        # exit when game is won
        if game.game_won():
            # print final gameboard state and total number of input and valid moves
            print(" "+game.give_board())
            print(command_count)
            print("Congratulations, you have won the game!")

            # write all valid moves to output file
            with open('data/output_files/output.csv', 'a') as outputfile:
                outputfile.write(command_list)

            exit(0)
        
