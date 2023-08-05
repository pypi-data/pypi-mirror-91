# this file takes in the user input & uses the tic_tac_toe class
from .tic_tac_toe import TicTacToe

theBoard = {'7': ' ' , '8': ' ' , '9': ' ' ,
            '4': ' ' , '5': ' ' , '6': ' ' ,
            '1': ' ' , '2': ' ' , '3': ' ' }

ttt_object = TicTacToe(theBoard, response='y')