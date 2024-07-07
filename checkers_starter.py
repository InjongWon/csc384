import argparse
import copy
import sys
import time

NW = (-1, -1)
NE = (1, -1)
SW = (-1, 1)
SE = (1, 1)

cache = {} # you can use this to implement state caching!

class State:
    # This class is used to represent a state.
    # board : a list of lists that represents the 8*8 board
    def __init__(self, board, turn = 'r'):

        self.board = board
        self.turn = turn 
        self.width = 8
        self.height = 8
        self.king = False

    def display(self):
        for i in self.board:
            for j in i:
                print(j, end="")
                # if self.board[i]
            print("")
        print("")

    def clone(self):
        new_board = copy.deepcopy(self.board)
        return State(new_board, self.turn)
    
def get_opp_char(player):
    if player in ['b', 'B']:
        return ['r', 'R']
    else:
        return ['b', 'B']

def get_next_turn(curr_turn):
    if curr_turn == 'r':
        return 'b'
    else:
        return 'r'

def read_from_file(filename):

    f = open(filename)
    lines = f.readlines()
    board = [[str(x) for x in l.rstrip()] for l in lines]
    f.close()

    return board

def in_bound(m, n):
    """checking whether the [row][col] is in bound"""
    if m < 0 or n < 0 or m > 7 or n > 7:
        return False
    else: 
        return True

def check_king(turn, row):
    if state.turn == 'r' and row == 0:
        return True
    if state.turn == 'b' and row == 7:
        return True

def can_jump(state, row, col, newRow,newCol):
    # checking if the boards[][] piece is able to jump
    eat_opp_row, eat_opp_col = (row + newRow), (col+newCol)
    jumpRow, jumpCol = row + 2 * newRow, col + 2 * newCol
    
    return (in_bound(eat_opp_row, eat_opp_col) and
            in_bound(jumpRow, jumpCol) and
            state.board[eat_opp_row][eat_opp_col] in get_opp_char(state.turn) and
            state.board[jumpRow][jumpCol] == '.')


def execute_jump(state, row, col, newRow, newCol):
    eat_opp_row, eat_opp_col = row + newRow, col + newCol
    jumpRow, jumpcol = row + 2 * newRow, col + 2 * newCol
    new_state = state.clone()
    # swap 2 places 
    new_state[jumpRow][jumpcol], new_state[row][col] = new_state[row][col], '.' 
    new_state[eat_opp_row][eat_opp_col] = '.'
    
    return new_state, jumpRow, jumpcol


def get_jump_recursive(state, row, col, directions):
    """ This return all the possible jump moves if there is, in the current state.

        direction: diagonal, NE,NW,SW,SE
    """
    #current piece in current state
    current_piece = state.board[row][col]
    # array to return all jumps including multi jumps 
    jumps = []
    # initialize to find if there are jumps 
    found_jump = False
    # go through all directions (-1,-1), (-1,1), (1, -1) (1,1)
    for x,y in directions:
        # check if the piece can make valid jump
        if can_jump(state,row,col, x, y):
            #perform jump
            new_state, jumpRow, jumpCol = execute_jump(state,row, col, x, y)
            # check after making jump, if you can make multiple jump -> double 
            multiple_jumps = get_jump_recursive(new_state, jumpRow,jumpCol, directions)
            #check if there is multiple jumps then add it to the possible jump moves
            if multiple_jumps:
                #if so, add the double jump to the jump array 
                jumps.extend(multiple_jumps)
            else:
                jumps.append(multiple_jumps)
    # if there is no jumps then 
    if not jumps:
        # change to the opponent 
        state.turn = get_next_turn(state.turn)
        jumps.append(state)
        
    return jumps 

def get_simple_move(state, row, col, nr, nc):
    moves = []
    new_row, new_col = row + nr, col + nc 
    # Check if the new position is within bounds and is unoccupied
    if in_bound(new_row, new_col) and state.board[new_row][new_col] == '.':
        new_state = state.clone()
        #set current position -> '.' and new position to the piece coordinate. 
        new_state.board[new_row][new_col], new_state.board[row][col] = state.board[row][col], '.'
        if check_king(new_state.board[new_row][new_col], new_row):
            new_state.board[new_row][new_col] = new_state.board[new_row][new_col].upper()
        new_state.turn = get_next_turn(state.turn)
        moves.append(new_state)
    return moves
    
def find_simple_moves(state, row, col):
    
    moves = []

    current = state.board[row][col]
    if current in ['r', 'b']:
        directions = [(1, 1), (1, -1)] if current == 'b' else [(-1, 1), (-1, -1)]
    elif current in ['R', 'B']:
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    for nr, nc in directions:
        moves.extend(get_simple_move(state, row, col, nr, nc))

    return moves


   



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--inputfile",
        type=str,
        required=True,
        help="The input file that contains the puzzles."
    )
    parser.add_argument(
        "--outputfile",
        type=str,
        required=True,
        help="The output file that contains the solution."
    )
    args = parser.parse_args()

    initial_board = read_from_file(args.inputfile)
    state = State(initial_board)
    turn = 'r'
    ctr = 0

    sys.stdout = open(args.outputfile, 'w')

    sys.stdout = sys.__stdout__

# def update_coordinates(curr_coord,x,y):
#     curr_x,curr_y = curr_coord
#     new_row = curr_x + x
#     new_col = curr_y + y 
#     return new_row, new_col

# def get_simple_move(state, row, col, nr, nc):
#     moves = []
#     newRow, newCol = update_coordinates((row,col), nr, nc)
    
#     if in_bound(newRow,newCol) and state.board[newRow][newCol] == '.':
#         new_state = state.clone()
#         new_state.board[newRow][newCol], new_state.board[row][col] = state.board[row][col], '.' #switching new and clearing old
#         if check_king(new_state.board[newRow][newCol], row):
#             #change the piece to B or R 
#             new_state.board[newRow][newCol] = new_state.board[newRow][newCol].upper()
#         new_state.turn = get_next_turn(state.turn)
#         moves.append(new_state)
#     return moves 

# def generate_successors(state):
#     simple, jumps = [], []
    
#     for row in range(state.height):
#         for col in range(state.width):
#             if state.board[row][col].lower() == state.turn:
#                 possible_moves = find_moves(state,row,col)
                
    
#     if jumps:
#         return jumps
#     return simple
 