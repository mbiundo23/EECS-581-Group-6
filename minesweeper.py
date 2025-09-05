import random

def getNeighbors(num): # Helps narrow the spaces to check bombs for a given space
        # First, we'll classify the num as LeftEdge or RightEdge
        isLeftEdge = False
        isRightEdge = False
        if ((num-1)%10) == 0: # This singles out 1, 11, 21, 31, etc as left edges.
                isLeftEdge = True
        if (num%10) == 0: # This singles out 10, 20, 30, 40, as right edges.
                isRightEdge = True
        neighbors = []
        if not isRightEdge:
                neighbors.append(num + 1) # Add right
        if not isLeftEdge:
                neighbors.append(num - 1) # Add left
        if (num + 10 < 101):
                neighbors.append(num + 10) # Add down
        if (num - 10 > 0):
                neighbors.append(num - 10) # Add up
        if (not isLeftEdge) and (num-10 > 0):
                neighbors.append(num - 11) # Add up-left
        if (not isRightEdge) and (num-10 > 0):
                neighbors.append(num - 9) # Add up-right
        if (not isLeftEdge) and (num+10 < 101):
                neighbors.append(num + 9) # Add down-left
        if (not isRightEdge) and (num+10 < 101):
                neighbors.append(num + 11) # Add down-right
        return neighbors

def initBoard(bomb_ct, bomb_spaces):
        board = [] # We initialize an array.
        for i in range(1, 102): # Range fills indices 1-100.
                board.append(0) # We fill array with 0's.
        for i in range(len(bomb_spaces)):
                bomb_idx = bomb_spaces[i] # Get location of bomb
                board[bomb_idx] = '*' # Insert bomb character

        # Now we just need to fill values around bombs!

        for i in range(1, len(board)): # For every space in the board we need to find how many bombs are around it.
                if (board[i] == '*'):
                        continue # We don't need the value where bombs are so we skip.
                space_val = 0
                neighbors = getNeighbors(i) # We'll get the valid indices in separate function.
                for index in neighbors: # Iterate through neighbor list
                        if (board[index] == '*'): # If the board at that neighbor is a bomb...
                                space_val += 1 # ...increment space value
                board[i] = space_val # Set value at that board space.
        # Once we're done iterating, the board is all set up!
        return board

def printBoard(board):
        i = 0
        string = ''
        for j in range(len(board)):
                if j == 0:
                        continue
                string += str(board[j]) + ' '
                i += 1
                if i == 10:
                        print(string)
                        i = 0
                        string = ''
        return

def displayBoard(display):
        print('    A  B  C  D  E  F  G  H  I  J  ')
        test_string = ''
        for i in range(10):
                for j in range(10):
                        test_string += '[' + str(display[(((i*10)+j)+1)]) +']' #In final implement, print something between brackets
                if (i+1 != 10):
                        print(str(i+1) + '  ' + test_string)
                else:
                        print(str(i+1) + ' ' + test_string)
                test_string = ''
        return

def main():
        print('Welcome to Minesweeper!') # Welcome the player!
        bomb_ct = int(input('How many bombs should there be?: ')) # Get bomb count!
        bomb_spaces = random.sample(range(1, 101), bomb_ct) # Get random position of bombs.
        board = initBoard(bomb_ct, bomb_spaces) # Generate board
        display = [] # Generate display board
        for i in range(101):
                display.append(' ') # For now fill it with empty space
        print('\n')
        displayBoard(display)
        print('\n')
        printBoard(board)
        print('\n')
        for i in range(len(board)):
                display[i] = board[i]
        displayBoard(display)
        return
main()
