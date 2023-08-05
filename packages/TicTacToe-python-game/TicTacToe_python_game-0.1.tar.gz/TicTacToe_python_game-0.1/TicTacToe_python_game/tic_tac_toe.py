import os

class TicTacToe:
    '''
    This class takes in the user input, displays board and calculates next move
    '''
    def __init__(self, board, response):
        '''
        Arguments:
        board represents the dictionary type of a tic tac toe board defined in main
        response represents the response of the user whether he/she wants to play more or not (default = 'y')
        '''
        self.board = board
        self.restart = response
        self.board_keys = []
        self.check_response(self.board_keys)

        for key in self.board:
            self.board_keys.append(key)

    def check_response(self, restart):
        '''
        Checks the response after each game for either continuing or exiting game

        Arguments: restart represents whether a user wants a rematch or not (y/n)
        '''
        if self.restart == "y" or self.restart == "Y":  
            self.game_play()
        elif self.restart == "n" or self.restart == "N":
            print('Exiting, have a good day!')
        else:
            print('Invalid input, exiting')

    def print_board(self):	
        '''
        Prints the updated board after each move
        '''
        print(self.board['7'] + '|' + self.board['8'] + '|' + self.board['9'])
        print('-+-+-')
        print(self.board['4'] + '|' + self.board['5'] + '|' + self.board['6'])
        print('-+-+-')
        print(self.board['1'] + '|' + self.board['2'] + '|' + self.board['3'])

    def game_play(self):
        '''
        Defines how the game is played
        '''

        turn = 'X'
        count = 0
        new_key = {'7': ' ' , '8': ' ' , '9': ' ' ,
                   '4': ' ' , '5': ' ' , '6': ' ' ,
                   '1': ' ' , '2': ' ' , '3': ' ' }

        # for each key in the above dictionary, make the corresponding value null
        for key in new_key:
            new_key[key] = " "

        # update the board using the new_key
        self.board = new_key
        
        # clear screen before starting the game
        os.system('cls')

        # print the board before game
        self.print_board()
        
        # requires 9 moves to predict a winner, hence from 0 to 8
        for i in range(9):            
            # select position from 1 to 9
            move = input('Move to which place?')

            # check if position you entered is empty.
            if self.board[move] == ' ':
                # if empty, assign either X or 0 depending on the turn of the user
                self.board[move] = turn
                count += 1
            else:
                print('That position is already filled, play in some other position')
                continue

            # clear screen before starting the game
            os.system('cls')

            # print board with updated values
            self.print_board()

            # if count is greater than or equal to 5, there could be a combination of 3 X's or 3 0's to win
            if count >= 5:
                # across the top
                if self.board['7'] == self.board['8'] == self.board['9'] != ' ': 
                    print("\nGame Over.\n")             
                    print(turn + " WON\n")
                    break
                # across the middle
                elif self.board['4'] == self.board['5'] == self.board['6'] != ' ': 
                    print("\nGame Over.\n")             
                    print(turn + " WON\n")
                    break
                # across the bottom
                elif self.board['1'] == self.board['2'] == self.board['3'] != ' ': 
                    print("\nGame Over.\n")             
                    print(turn + " WON\n")   
                    break
                # down the left side
                elif self.board['1'] == self.board['4'] == self.board['7'] != ' ': 
                    print("\nGame Over.\n")             
                    print(turn + " WON\n")
                    break
                # down the middle
                elif self.board['2'] == self.board['5'] == self.board['8'] != ' ': 
                    print("\nGame Over.\n")             
                    print(turn + " WON\n")
                    break
                # down the right side
                elif self.board['3'] == self.board['6'] == self.board['9'] != ' ': 
                    print("\nGame Over.\n")             
                    print(turn + " WON\n")
                    break 
                # diagonal
                elif self.board['7'] == self.board['5'] == self.board['3'] != ' ': 
                    print("\nGame Over.\n")                
                    print(turn + " WON\n")
                    break
                # diagonal
                elif self.board['1'] == self.board['5'] == self.board['9'] != ' ': 
                    print("\nGame Over.\n")                
                    print(turn + " WON\n")
                    break 
                    
            # if all cells are filled and no one has any combination of 3 X's or 0's, the game has tied
            if count == 9:
                print('Game Over, it is a TIE')

            # keep alternating between the two players
            if turn =='X':
                turn = 'O'
            else:
                turn = 'X'      

        # clear system console
        self.restart = input('Do you want to play again? (y/n)\nAnswer: ')
        self.check_response(self.restart)

