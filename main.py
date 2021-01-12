

from code.classes.game import Game # dit werkt niet...

import csv
from sys import argv

if __name__ == "__main__":

    # check if command lina arguments are given
    if len(argv) != 3:
        print("Usage: python main.py [game_number] [board_dimention]")
        exit(1)
    
    # check game number
    if int(argv[1]) not in range(8):
        print("Invalid game number")
        exit(1)

    # check board dimension
    if int(argv[2]) not in [6, 9, 12]:
        print("Invalid board dimension")
        exit(1)

    # load game
    game_number, board_dimension = argv[1], argv[2]
    game = Game(board_dimension, game_number)

    # initiate output file
    with open('data/output_files/output.csv', 'w', newline ='') as outputfile:
        writer = csv.writer(outputfile)
        writer.writerow(["car", "move"])
        

    print("Enter a move in the folowing format:\n[car_id],[move]\n" +
            "when you want to move left or up, enter a negative number.")

    print(" "+game.give_board())
    
    # prompt user for commands
    while True:
        command = input("> ").upper()

        if "," not in command:
            print("Invalid command. Enter a move in the folowing format:\n[car_id],[move]")
            continue
        
        command = command.split(",")
        # check if move is valid
        if not game.valid_move(*command):
            print("Invalid move")
            continue

        # perform move an print current board
        game.move(*command)
        print(" "+game.give_board())

        # write the move to the output file
        with open('data/output_files/output.csv', 'a') as outputfile:
            writer = csv.writer(outputfile)
            writer.writerow([*command])

        # exit when game is won
        if game.game_won():
            print("Congratulations, you have won the game!")
            exit(0)
        
