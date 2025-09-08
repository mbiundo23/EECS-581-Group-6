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

def generateBoard(bomb_ct, bomb_spaces):
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

def printBoard(board): # DEBUG FUNCTION TO SEE BACKGROUND BOARD STATE IN ROUGHLY USER FORMAT
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

def displayBoard(display): # FUNCTION TO DISPLAY USER'S BOARD
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

def getInput(): # We can flesh this out with error handling later.
        inp_string = input("Please give command: ") # Ask for command.
        com_type = inp_string[0] # Parse first character for command type ("m" or "f")
        inp_string = inp_string[1:len(inp_string)] # Remove first character from input string.
        
        col = inp_string[len(inp_string)-1] # Look at end of input string for column letter.
        cols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'] # Bank of possible letters.
        col = cols.index(col) + 1 # Translate that column into numerical column position.
        inp_string = inp_string[:len(inp_string)-1] # Remove last character from input string.
        
        row = int(inp_string) # What's remaining of input string should be row number.
        
        command = [] # Create command value.
        command.append(com_type) # Add the "m" or "f"
        command.append(row) # Add row number.
        command.append(col) # Add column number.
        
        return command # Return parsed input.

def main():
        # DISPLAY CREATION
        display = []
        for i in range(101):
                display.append(' ') # For now fill it with empty space

        # GAME START
        print('Welcome to Minesweeper!') # Welcome the player!
        bomb_ct = int(input('How many bombs should there be?: ')) # Get bomb count!
        displayBoard(display) # Show empty display to user.

        bomb_spaces = random.sample(range(1, 101), bomb_ct) # Get random position of bombs.
        user_input = getInput() # Get first user input as list in command type, column, row format
        space = ((user_input[1]-1)*10) + user_input[2] # Translate col and row into actual board space.
        
        # SPACE-BOMB COLLISION PROBLEM
        if space in bomb_spaces:
                problem_index = bomb_spaces.index(space) # Isolate where in the list of bomb spaces the user space and bomb collide.
                while space == bomb_spaces[problem_index]: # While these two values are the same...
                        bomb_spaces[problem_index] = random.randint(1, 100) # ...we will reroll that bomb space.
                        i = 0 # Then we'll check how many times the new value appears.
                        for place in bomb_spaces: # Check every bomb space
                                if bomb_spaces[problem_index] == place: # If the new space appears in bomb spaces, increment.
                                        i += 1 # This should increment only once (when the new space compares itself).
                        if i > 1: # If the new bomb space increments multiple times, we still have a collision.
                                bomb_spaces[problem_index] = space # We can't let the while loop end so reset with space.

        # CALL BOARD GENERATION                        
        board = generateBoard(bomb_ct, bomb_spaces)
        
        # UPDATE BOARD
        display[space] = board[space] # for now this is a placeholder. this should be a real function that propogates value.
        
        # PRINT DISPLAY FOR USER
        print('\n')
        displayBoard(display) # Print display
        
        # DEBUG LINES
        print('\n')
        printBoard(board)
        
        # GAME LOOP BEGINS
        
        return
main()
