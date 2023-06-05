"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None

LEN = 3 # length of the multidimensional list 

import copy


def initial_state():
    """
    Returns starting state of the board.
    Initially the board is left empty 
    This is an example of a board state 
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    Following the alternating logic of the game 
    
    """
    # If it is a terminal state board return None (terminal board includes one that is already won or no more moves possible)
    # else look at the player that has more moves on the board, the next turn would be the other players

    if terminal(board):
        return None

    moves = 0
    # If its even number of turns on the board it is X's turn
    # Else if its odd number of turns on the board it is O's turn 
    for row in range(LEN):
        for col in range(LEN):
            if board[row][col] is not EMPTY:
                moves += 1
    if moves == 0 or moves % 2 == 0:
        return X
    else:
        return O
    

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # Check if not terminal board:
    #   loop through all empty cells (3 by 3) multidimensional list would have a cost of n raised to 3. Any better way ?
    if terminal(board):
        return None
    acts = set()
    for row in range(LEN):
        for col in range(LEN):
            if board[row][col] == EMPTY:
                acts.add((row, col))
    return acts

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Make a deep copy of the board and update it with action and return the resulting board
    cp = copy.deepcopy(board) # Make a deep copy of the board
    turn = player(board) # figure out which players turn it is, turn would be a shallow copy I suppose
    row = action[0]; col = action[1]                                
    if cp[row][col] is not EMPTY:
        raise ValueError
    cp[row][col] = turn # update the copied board
    return cp


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Return winner of the board if there is one 
    # Assume no invalid states exist such as both players winning at once 
    # horizontally, vertically and diagonally 
    # check for a vertical win
    for col in range(LEN):
        if (board[0][col] == board[1][col]) and (board[1][col] == board[2][col]): # if all cells in a column have identical values
            if board[0][col] == X:
                return X
            elif board[0][col] == O:
                return O
        # check for a horizontal win
    for row in range(LEN):
        if (board[row][0] == board[row][1]) and (board[row][1] == board[row][2]):
            if board[row][0] == X:
                return X
            elif board[row][0] == O:
                return O
        # check for a first diagonal win 
    if (board[0][0] == board[1][1]) and (board[1][1] == board[2][2]):
        if board[0][0] == X:
            return X
        elif board[0][0] == O:
            return O
    # check for a second diagonal win
    if (board[0][2] == board[1][1]) and (board[1][1] == board[2][0]):
        if board[0][2] == X:
            return X
        elif board[0][2] == O:
            return O
    return None # if the board is in progress just return None
    
    
        
        
def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # When do we have a terminal state board 
    # If the game is already won: therefore, two diagonal and one across 
    # If the game board has a time 
    if winner(board) is not None: # if there is a winner we have a terminal board
        return True
    # else if all cells in the board are full then we have a terminal board 
    for row in range(LEN):
        for col in range(LEN):
            if board[row][col] == EMPTY:
                return False
    return True

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # If x won utility is 1 else if O then -1 else it is 0
    # Assume utility will only be called if terminal(board) is True
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else: 
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # if the entire board is empty 
    if is_empty(board):
        # generate goal action randomly 
        return (0, 0)
    current_player = player(board) # get the current player of the board
    goal_action = None
    if current_player == X:
        previous_val = -math.inf
        for action in actions(board):
            if max(previous_val, min_value(result(board, action))) is not previous_val:
                goal_action = action
                previous_val = min_value(result(board, action))
    elif current_player == O:
        previous_val = math.inf
        for action in actions(board):
            if min(previous_val, max_value(result(board, action))) is not previous_val:
                goal_action = action
                previous_val = max_value(result(board, action))
    return goal_action
    
def max_value(board):
    if terminal(board):
        return utility(board)
    v = -math.inf
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v

def min_value(board):
    if terminal(board):
        return utility(board)
    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v 

def is_empty(board):
    for row in range(LEN):
        for col in range(LEN):
            if board[row][col] is not EMPTY:
                return False
    return True
