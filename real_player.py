def find_move(board):
    pos = 0
    global InARow 
    InARow = 0
    #look for patterns
        #--> 1 or 2 in a row
            #-->set either(self or other -->winn + defens)
        #--> else look poistion in wich you can winn or have a good start
    return set(board,pos)
def set(board,pos):
    board[pos] = 4
    return board