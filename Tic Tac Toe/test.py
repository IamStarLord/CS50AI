import tictactoe as ttt

def main():
    board = [ [ttt.EMPTY, ttt.EMPTY, ttt.EMPTY],
              [ttt.EMPTY, ttt.EMPTY, ttt.EMPTY],
              [ttt.EMPTY, ttt.EMPTY, ttt.EMPTY] ]

    #print(ttt.player(board)) Player function works correctly
    #print(ttt.actions(board)) Actions function works correctly
    #print(ttt.result(board, (0, 1))) Result fuction works correctly
    #print(ttt.winner(board)) winner function works correctly
    #print(ttt.terminal(board)) terminal function works correctly
    print(ttt.minimax(board))

if __name__ == "__main__":
    main()