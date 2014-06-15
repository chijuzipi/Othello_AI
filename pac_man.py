import struct, string
import sys
from time import time
from copy import deepcopy
import random

class pac_man:

    #def __init__(self):
    def __init__(self, cpu, human):
        sys.setrecursionlimit(150000)
        self.board = [[' ']*8 for i in range(8)]
        self.size = 8
        self.board[4][4] = chr(10084) 
        self.board[3][4] = chr(9762)
        self.board[3][3] = chr(10084)
        self.board[4][3] = chr(9762) 
        self.level = 0
        self.cpu = cpu
        self.human = human
        # a list of unit vectors (row, col)
        self.directions = [ (-1,-1), (-1,0), (-1,1), (0,-1),(0,1),(1,-1),(1,0),(1,1)]

#prints the boards
    def PrintBoard(self):

        # Print column numbers
        print()
        print("  ",end="")
        print("1  2  3  4  5  6  7  8")
# Build horizontal separator
        #linestr = " " + ("+-" * self.size) + "+"
        linestr = " " + ("---" * self.size) + "-"

        # Print board
        #endSambol = chr(8198)+ "|"
        endSambol = chr(8202)+ "|"
        for i in range(self.size):
            print(linestr)                     # Separator
            print(i+1,end="|")                 # Row number
            for j in range(self.size): print(self.board[i][j],end=endSambol)  # board[i][j] and pipe separator 
            print()                           # End line
        print(linestr)

#checks every direction fromt the position which is input via "col" and "row", to see if there is an opponent piece
#in one of the directions. If the input position is adjacent to an opponents piece, this function looks to see if there is a
#a chain of opponent pieces in that direction, which ends with one of the players pieces.   
    def islegal(self, row, col, player, opp):
        if(self.get_square(row,col)!=" "):
            return False
        for Dir in self.directions:
            for i in range(self.size):
                if  ((( row + i*Dir[0])<self.size)  and (( row + i*Dir[0])>=0 ) and (( col + i*Dir[1])>=0 ) and (( col + i*Dir[1])<self.size )):
                    #does the adjacent square in direction dir belong to the opponent?
                    if self.get_square(row+ i*Dir[0], col + i*Dir[1])!= opp and i==1 : # no
                        #no pieces will be flipped in this direction, so skip it
                        break
                    #yes the adjacent piece belonged to the opponent, now lets see if there are a chain
                    #of opponent pieces
                    if self.get_square(row+ i*Dir[0], col + i*Dir[1])==" " and i!=0 :
                        break

                    #with one of player's pieces at the other end
                    if self.get_square(row+ i*Dir[0], col + i*Dir[1])==player and i!=0 and i!=1 :
                        #set a flag so we know that the move was legal
                        return True
        return False
        
#returns true if the square was played, false if the move is not allowed
    def place_piece(self, row, col, player, opp):
        if(self.get_square(row,col)!=" "):
            return False
        
        if(player == opp):
            print("player and opponent cannot be the same")
            return False
        
        legal = False
        #for each direction, check to see if the move is legal by seeing if the adjacent square
        #in that direction is occuipied by the opponent. If it isnt check the next direction.
        #if it is, check to see if one of the players pieces is on the board beyond the oppponents piece,
        #if the chain of opponents pieces is flanked on both ends by the players pieces, flip
        #the opponents pieces 
        for Dir in self.directions:
            #look across the length of the board to see if the neighboring squares are empty,
            #held by the player, or held by the opponent
            for i in range(self.size):
                if  ((( row + i*Dir[0])<self.size)  and (( row + i*Dir[0])>=0 ) and (( col + i*Dir[1])>=0 ) and (( col + i*Dir[1])<self.size )):
                    #does the adjacent square in direction dir belong to the opponent?
                    if self.get_square(row+ i*Dir[0], col + i*Dir[1])!= opp and i==1 : # no
                        #no pieces will be flipped in this direction, so skip it
                        break
                    #yes the adjacent piece belonged to the opponent, now lets see if there are a chain
                    #of opponent pieces
                    if self.get_square(row+ i*Dir[0], col + i*Dir[1])==" " and i!=0 :
                        break

                    #with one of player's pieces at the other end
                    if self.get_square(row+ i*Dir[0], col + i*Dir[1])==player and i!=0 and i!=1 :
                        #set a flag so we know that the move was legal
                        legal = True
                        self.flip_tiles(row, col, Dir, i, player)
                        break

        return legal

#Places piece of opponent's color at (row,col) and then returns 
#  the best move, determined by the make_move(...) function
    def play_square(self, row, col, playerColor, oppColor):     
        start_time = time()
        # Place a piece of the opponent's color at (row,col)
        if (row,col) != (-1,-1):
            put_tile(self, row, col,oppColor,playerColor)
        
        # Determine best move and and return value to Matchmaker
        #return self.make_test_move(playerColor, oppColor)
        return self.make_minimax_cpu_move(start_time, playerColor, oppColor)

#sets all tiles along a given direction (Dir) from a given starting point (col and row) for a given distance
# (dist) to be a given value ( player )
    def flip_tiles(self, row, col, Dir, dist, player):
        for i in range(dist):
            self.board[row+ i*Dir[0]][col + i*Dir[1]] = player
        return True
    
#returns the value of a square on the board
    def get_square(self, row, col):
        return self.board[row][col]

#Search the game board for a legal move, and play the first one it finds
    def make_test_move(self, playerColor, oppColor):
        for row in range(self.size):
            for col in range(self.size):
                if(self.islegal(row,col,playerColor, oppColor)):
                    self.place_piece(row, col, playerColor, oppColor)
                    return (row, col)
        return (-1, -1)
#-----------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------
    def print_moves(self, move_list):
        result = []
        for i in range(len(move_list)):
            result.append((move_list[i][0]+1, move_list[i][1]+1))
        return result
            
    # make a cpu move, in this case, using minimax with alpha/beta and an edge-play heuristic
    def make_simple_cpu_move(self, t, playerColor, oppColor):
        #get all the possible moves
        possible_moves = self.get_moves(playerColor, oppColor)
        if len(possible_moves) == 0:
            return (-1, -1)
        #shuffle the move
        random.shuffle(possible_moves)
        score_max = float("-inf") 
        move_max = None
        
        for move in possible_moves:
            row, col = move[0], move[1]
            if isCornerMove(move): 
                print('is a corner move!')
                self.place_piece(row, col, playerColor, oppColor)
                return (row, col)
        for move in possible_moves:
            row, col = move[0], move[1]
            if isEdgeMove(move): 
                print('is a edge move!')
                self.place_piece(row, col, playerColor, oppColor)
                return (row, col)
        for move in possible_moves:
            row, col = move[0], move[1]
            temp_board = deepcopy(self)
            put_tile(temp_board, row, col, playerColor, oppColor)
            score = get_score(temp_board, playerColor, oppColor)
            if score > score_max:
                score_max = score
                move_max = move
        print("find the max score!")
        self.place_piece(move_max[0], move_max[1], playerColor, oppColor)
        return (move_max[0], move_max[1]) 
    
    # make a cpu move, in this case, using minimax with alpha/beta and an edge-play heuristic
    def make_minimax_cpu_move(self, t, playerColor, oppColor):
        #get all the possible moves
        self.level = 0
        possible_moves = self.get_moves(playerColor, oppColor)
        move_numbers = len(possible_moves)
        if move_numbers == 0:
            return (-1, -1)
        if move_numbers == 1:
            move = possible_moves[0]
            self.place_piece(move[0], move[1], playerColor, oppColor)
            return (move[0], move[1])
            
        alpha = float("-inf")
        beta = float("inf")
        
        #Using iterative deepening algorithm
        #start from level limit 1
        levelLimit = 1
        while True: 
            #CPU player always tries to maximize the evaluatioin 
            move_this, score_this = self.maximize(self, t, alpha, beta, playerColor, oppColor, levelLimit)
            if move_this is not False:
            #did not terminated by time limit
                move = move_this
                score = score_this

            levelLimit += 1

            if time() - t > 14.5:
                print ("deepest level reach to: ", levelLimit)
                break

        if move is None:
            return (-1, -1)
        self.place_piece(move[0], move[1], playerColor, oppColor)
        print ("using time", (time()-t))
        print("CPU played row: " + str(move[0]+1) + " col: " + str(move[1]+1) + ", which had a score of " +
        str(score))
        return (move[0], move[1])

    # maximize the score when the cpu player is playing
    def maximize(self, board, t, alpha, beta, playerColor, oppColor, limit):
        #first increase deepth
        self.level += 1 
        score_max = float("-inf") 
        move_max = None
       
       #possible_moves = get_moves(board, playerColor, oppColor)
        possible_moves = get_moves(board, playerColor, oppColor)
        choices = len(possible_moves) 
        if choices == 0:
            return ((-1, -1), score_max)
        
        #always use copy of board, self board is never modeified
        # shuffle the possible move list so the cpu move will not be predicted if multiple moves have same score 
        random.shuffle(possible_moves)
        for move in possible_moves:
            temp_board = deepcopy(board)
            temp_board.place_piece(move[0], move[1], playerColor, oppColor)
            #if the game is finish (both two players dont have move) or level limit is reached, calculate the score
            if (has_move(temp_board, oppColor, playerColor) == False) and (has_move(temp_board,playerColor, oppColor) == False):
                score = get_score(temp_board, playerColor, oppColor)
            elif (self.level >= limit): 
                score = get_score(temp_board, playerColor, oppColor)
            elif (time()-t > 14.5): 
                return False, False 

            #make sure the calculation finish within 15 s
            else:
            # call the minimize, swap the players
                step, score = self.minimize(temp_board, t, alpha, beta, oppColor, playerColor, limit) 
                if step is False:
                    return False, False
            
            if (score > score_max):
                move_max = move 
                score_max = score 
                alpha = score_max
            if (score_max > beta):
                break
        # evey time return, step back from 1 level
        self.level -= 1 
        return (move_max, score_max)

    # minimize the score when the opp is playing 
    def minimize(self, board, t, alpha, beta, playerColor, oppColor, limit):
        self.level += 1 
        score_min = float("inf") 
        move_min = None
        possible_moves = get_moves(board, playerColor, oppColor)
        choices = len(possible_moves) 
        if choices == 0:
            return ((-1, -1), score_min)

        random.shuffle(possible_moves)
        for move in possible_moves:
            temp_board = deepcopy(board)
            temp_board.place_piece(move[0], move[1], playerColor, oppColor)

            if (has_move(temp_board, oppColor, playerColor) == False) and (has_move(temp_board,playerColor, oppColor) == False):
                score = get_score(temp_board, oppColor, playerColor)
            elif (self.level >= limit): 
                score = get_score(temp_board, oppColor, playerColor)
            elif (time() - t> 14.5): 
                return False, False 
            else:
            
                step, score = self.maximize(temp_board, t, alpha, beta, oppColor, playerColor, limit) 
                if step is False:
                    return False, False
            
            if (score < score_min):
                move_min = move 
                score_min = score 
                beta = score_min
            if (score_min < alpha):
                break
        self.level -= 1 
        return (move_min, score_min)

    def get_moves(self, player, opp):
        moves = []
        for row in range(self.size):
            for col in range(self.size):
                if self.islegal(row, col, player, opp):
                    moves.append((row, col))
        return moves

# Checks all board positions to see if there is a legal move
    def has_move(self, player, opp):
        for row in range(self.size):
            for col in range(self.size):
                if self.islegal(row, col, player, opp):
                    return True
        return False
    
    #determines the score of the board by adding +1 for every tile owned by player, and -1 for every tile owned by opp
    def score(self, playerColor, oppColor):
        scorePlayer = 0
        for row in range(self.size):
            for col in range(self.size):
                if self.get_square(row, col) == playerColor:
                    scorePlayer += 1
                if self.get_square(row, col) == oppColor:
                    scorePlayer -= 1
        return scorePlayer 
    
    # Check to see if the game is over
    def game_over(self, playerColor, oppColor):
        if (self.full_board() or self.all_pieces(playerColor, oppColor)):
            return True
        return False
    
    def full_board(self):
        for row in range(self.size):
            for col in range(self.size):
                if self.get_square(row, col) == ' ':
                    return False
        return True
    
    def all_pieces(self, playerColor, oppColor):
        hasPlayer = False
        hasOpp = False
        for row in range(self.size):
            for col in range(self.size):
                if self.get_square(row, col) == playerColor:
                    hasPlayer = True
                if self.get_square(row, col) == oppColor:
                    hasOpp = True
        if hasPlayer and hasOpp:
            return False
        return True
        
def get_moves(board, player, opp): 
    moves = [] 
    for row in range(board.size): 
        for col in range(board.size):
            if board.islegal(row, col, player, opp): 
                moves.append((row, col))
    return moves 
    
# Checks all board positions to see if there is a legal move
def has_move(board, player, opp): 
    for row in range(board.size): 
        for col in range(board.size):
            if board.islegal(row, col, player, opp): 
                return True 
    return False 
    
def isEdgeMove(move): 
    if  (move[0] in [1, 2, 3, 4, 5, 6]) and (move[1] in [0, 7]):
        return True
    if  (move[1] in [1, 2, 3, 4, 5, 6]) and (move[0] in [0, 7]):
        return True
    return False

def isCornerMove(move):
    if  move in [(0, 0), (0, 7), (7, 0), (7, 7)]:
        return True
    return False

def isBadMove(move): 
    if  (move[0] in [1, 2, 3, 4, 5, 6]) and (move[1] in [1, 6]):
        return True
    if  (move[1] in [1, 2, 3, 4, 5, 6]) and (move[0] in [1, 6]):
        return True
    return False

    
#This is the evaluation function
#determines the score of the board by adding +1 for every tile owned by player, and -1 for every tile owned by opp
def get_score(board, playerColor, oppColor):
    result = 0
    for row in range(board.size):
        for col in range(board.size):
            if board.get_square(row, col) == playerColor:
                if isCornerMove((row, col)):
                    result += 25 
                elif isEdgeMove((row, col)):
                    result += 5 
                elif isBadMove((row, col)):
                    result -= 5 
                else:
                    result += 1

            if board.get_square(row, col) == oppColor:
                if isCornerMove((row, col)):
                    result -= 25 
                elif isEdgeMove((row, col)):
                    result -= 5 
                elif isBadMove((row, col)):
                    result += 5 
                else:
                    result -= 1
    return result 

#returns true if the square was played, false if the move is not allowed
def put_tile(board, row, col, player, opp):
    if(board.get_square(row,col)!=" "):
        return False
    
    if(player == opp):
        print("player and opponent cannot be the same")
        return False
    
    legal = False
    #for each direction, check to see if the move is legal by seeing if the adjacent square
    #in that direction is occuipied by the opponent. If it isnt check the next direction.
    #if it is, check to see if one of the players pieces is on the board beyond the oppponents piece,
    #if the chain of opponents pieces is flanked on both ends by the players pieces, flip
    #the opponents pieces 
    for Dir in board.directions:
        #look across the length of the board to see if the neighboring squares are empty,
        #held by the player, or held by the opponent
        for i in range(board.size):
            if  ((( row + i*Dir[0])<board.size)  and (( row + i*Dir[0])>=0 ) and (( col + i*Dir[1])>=0 ) and (( col +
            i*Dir[1])<board.size )):
                #does the adjacent square in direction dir belong to the opponent?
                if board.get_square(row+ i*Dir[0], col + i*Dir[1])!= opp and i==1 : # no
                    #no pieces will be flipped in this direction, so skip it
                    break
                #yes the adjacent piece belonged to the opponent, now lets see if there are a chain
                #of opponent pieces
                if board.get_square(row+ i*Dir[0], col + i*Dir[1])==" " and i!=0 :
                    break

                #with one of player's pieces at the other end
                if board.get_square(row+ i*Dir[0], col + i*Dir[1])==player and i!=0 and i!=1 :
                    #set a flag so we know that the move was legal
                    legal = True
                    board.flip_tiles(row, col, Dir, i, player)
                    break

    return legal

def play(Game):
    Game.PrintBoard()
    print()
    
    # if the computer move first, since every spot give 
    # same evaluate at the beginning, just put on the center
    if (Game.cpu == chr(10084)):
        Game.place_piece(3, 2, Game.cpu, Game.human)
        print()
        print("CPU Move:")
        Game.PrintBoard()
        print()
    
    while (Game.has_move(Game.human, Game.cpu) or Game.has_move(Game.cpu, Game.human)):
        print("Is your turn!")
        print("Please pick a row")
        temp_input1 = input()
        print("Please pick a column")
        temp_input2 = input()

        try:
            row = int(temp_input1) - 1
            col = int(temp_input2) - 1
            if (row < 0) or (row > 7):
                print("Invalid move, please enter an valid one.")
                continue

            # Validate index
            if not Game.islegal(row, col, Game.human, Game.cpu):
                print("Invalid move, please enter an valid one.")
                continue
            else:
                Game.place_piece(row, col, Game.human, Game.cpu)
                if (not Game.has_move(Game.human, Game.cpu)):
                    break
                # let CPU move
                else:
                    Game.PrintBoard()
                    print()
                    print("CPU Move:")
                    start = time()
                    Game.make_minimax_cpu_move(start, Game.cpu, Game.human)
                    Game.PrintBoard()
                    print()

        except ValueError:
            print("Please enter an integer index")

    # Print game results
    print()
    print("Game over:")
    Game.PrintBoard()
    cpu, human = Game.score(Game.cpu, Game.human)
    print ('cpu scores:', cpu, 'human scores:', human)

# Main function
def main():
    print()
    print ('Welcome to Othello TeamD!')
    print()

    #mark if the game is on play '1', or finished
    onPlay = -1

    # Validate user input
    while (onPlay == -1):
        print("Please enter which player you would like to be, either good heart(1) or evil weapon(2): ", end="")
        player = input()

        # Setup game based on user choice
        try:
            if (player == '1'):
                Game = pac_man(chr(9762), chr(10084))
                play(Game)
                onPlay = 1
            elif (player == '2'):
                Game = pac_man(chr(10084), chr(9762))
                play(Game)
                onPlay = 1
            else:
                print ("Please enter either 1 or 2")
                onPlay = -1

        except ValueError:
            print ('valueError')
            onPlay = -1

if __name__ == '__main__':
    main()




















    
