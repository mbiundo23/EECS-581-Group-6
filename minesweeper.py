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

def propagate(space, display, board):
        display[space] = board[space]
        neighbors = getNeighbors(space)
        for neighbor in neighbors:
                if board[neighbor] == 0 and display[neighbor] != 'F':
                        if display[neighbor] != 0:
                                propagate(neighbor, display, board)
                elif display[neighbor] == 'F':
                        continue
                else:
                        display[neighbor] = board[neighbor]

def generateBoard(bomb_spaces): # Create background board with bombs and numerical values.
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

def printBoard(board): # DEBUG FUNCTION TO SEE BACKGROUND BOARD STATE IN ROUGHLY USER DISPLAY FORMAT
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

def displayBoard(display, status, bomb_ct, flag_ct): # FUNCTION TO DISPLAY USER'S BOARD
        print('\n    A  B  C  D  E  F  G  H  I  J  ')
        test_string = ''
        for i in range(10):
                for j in range(10):
                        test_string += '[' + str(display[(((i*10)+j)+1)]) +']'
                if (i+1 != 10): # Prints rows with built string above.
                        print(str(i+1) + '  ' + test_string)
                else: # Row 10 requires less space between itself and test string.
                        print(str(i+1) + ' ' + test_string)
                test_string = '' # Empty test string.
        print("Current status:", status)
        print("Mines remaining:", bomb_ct - flag_ct, "\n")
        return

def getInput(): # Parses given command into usable interpretation for program.
        i = True
        while i:
                try:
                        inp_string = input('Please give command: ') # Ask for command.
                        com_type = inp_string[0].lower() # Parse first character for command type ("m" or "f")
                        if com_type != 'm' and com_type != 'f':
                                raise
                        inp_string = inp_string[1:len(inp_string)] # Remove first character from input string.
        
                        col = inp_string[len(inp_string)-1] # Look at end of input string for column letter.
                        cols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'] # Bank of possible letters.
                        if col not in cols:
                                raise
                        col = cols.index(col) + 1 # Translate that column into numerical column position.
                        inp_string = inp_string[:len(inp_string)-1] # Remove last character from input string.
        
                        row = int(inp_string) # What's remaining of input string should be row number.
                        if row not in range(1, 11):
                                raise
                        i = False
                except:
                        print('\nCommand is faulty please follow command, row, column format.')
                        print('(Hint 1: To mine at row 1, column a, type "m1a")')
                        print('(Hint 2: To flag at row 7, column g, type "f7g")\n')
                        continue
        
        command = [] # Create command value.
        command.append(com_type) # Add the "m" or "f"
        command.append(row) # Add row number.
        command.append(col) # Add column number.
        
        return command # Return parsed input.

def main():
        # PLAY METADATA CREATION
        status = 'Playing'
        flag_ct = 0 # Track how many flags have been placed. Helps show remaining mines.
        
        # DISPLAY CREATION
        display = []
        for i in range(101):
                display.append(' ') # For now fill it with empty space

        # GAME START
        print('Welcome to Minesweeper!') # Welcome the player!

        # COLLECT BOMB AMOUNT (DIFFICULTY)
        i = 0
        while i == 0: # This while loop is purely for error handling. We don't stop asking until we get workable input!
                try:
                        bomb_ct = int(input('How many bombs should there be?: '))
                        if bomb_ct < 10 or bomb_ct > 20: # Bomb count must be between 10 and 20 per the requirements.
                                raise
                        i = 1
                except:
                        print("Invalid bomb count. Please input again.")

        # INITIAL GAME SETUP (DISPLAY AND BOMB LOCATIONS)
        displayBoard(display, status, bomb_ct, flag_ct) # Show empty display to user.
        bomb_spaces = random.sample(range(1, 101), bomb_ct) # Get random position of bombs. Not placed on board yet.

        # FIRST INPUT
        i = 0
        while i == 0: # We loop here, placing flags until we get the first 'mine' command.
            user_input = getInput() # Helper function gives us actionable command.
            space = ((user_input[1]-1)*10) + user_input[2] # Translate col and row from input into board space.
            
            if user_input[0] == 'f': # If we got a flag command, we place the flag on display.
                if display[space] == ' ': # Empty space means flag is allowed.
                                if flag_ct + 1 > bomb_ct: # Also got to check that we don't place too many flags.
                                        print("Cannot flag any more spaces. Please unflag with flag command.")
                                else:
                                        display[space] = 'F' # Put a flag on the display!
                                        flag_ct += 1 # Increment the amount of flags on board.
                elif display[space] == 'F': # Flag exists in current space, remove it.
                    display[space] = ' ' # Set flag to empty space.
                    flag_ct -= 1 # Decrement the amount of flags on board.
                displayBoard(display, status, bomb_ct, flag_ct) # Display the board to the user and loop again!
            elif user_input[0] == 'm': # We have a mine command!
                if display[space] == 'F': # Are we mining on a flag space?
                        print('Cannot flag given space.') # The loop continues...
                else:
                        i = 1 # Escape the loop.
        
        # SPACE-BOMB COLLISION PROBLEM
        if space in bomb_spaces: # In the event the selected space is where a mine was planned to be...
                problem_index = bomb_spaces.index(space) # Isolate where in the list of bomb spaces the user space and bomb collide.
                while space == bomb_spaces[problem_index]: # While these two values are the same...
                        bomb_spaces[problem_index] = random.randint(1, 100) # ...we will reroll that bomb space.
                        i = 0 # Then we'll check how many times the new bomb space value appears.
                        for place in bomb_spaces: # Check every bomb space
                                if bomb_spaces[problem_index] == place: # If the new space appears in bomb spaces, increment.
                                        i += 1 # This should increment only once (when the new space compares itself).
                        if i > 1: # If the new bomb space increments multiple times, we still have a collision.
                                bomb_spaces[problem_index] = space # We can't let the while loop end so reset with space.

        # CALL BOARD GENERATION                        
        board = generateBoard(bomb_spaces)
        
        # UPDATE BOARD w/ FIRST SPACE
        if board[space] == 0:
                propagate(space, display, board) # Reveal spaces around the 0 space.
        else:
                display[space] = board[space] # Reveal the space itself (it can't be a bomb)
        
        # GAME LOOP BEGINS
        while status == "Playing":
                displayBoard(display, status, bomb_ct, flag_ct)
                # printBoard(board) # this helps look at background board to compare against display
                user_input = getInput()
                space = ((user_input[1]-1)*10) + user_input[2] # Translate col and row into actual board space.
                
                # DIFFERENTIATE COMMAND TYPE (FLAG VS MINE COMMAND)

                #FLAG SCENARIO
                if user_input[0] == 'f':
                        if display[space] == ' ': # Empty space eligible for flagging
                                if flag_ct + 1 > bomb_ct: # Do we still have flags to use?
                                        print("Cannot flag any more spaces. Please unflag with flag command.")
                                else:
                                        display[space] = 'F' # Put flag on display.
                                        flag_ct += 1 # Increment the amount of flags.
                        elif display[space] == 'F': # Flag exists in current space, remove it.
                                display[space] = ' ' # Remove flag and empty display space.
                                flag_ct -= 1 # Decrement the amount of flags.
                        else: # If the space isn't empty or flagged, must be a value. We can't flag this.
                                print("Cannot flag given space.")

                #MINE SCENARIO
                elif user_input[0] == 'm':
                        # There's a few things we check here:
                                # Is the space a bomb?
                                # Is the space a flag?
                                # Is the space 0?
                                # Is the space any other value?
                        # We will check if the space is a flag first.
                        if display[space] == "F":
                                print("Cannot mine here. Flag is in the way.")# We don't actually do anything. We just say a flag is in the way.
                        # We will check if the space is a bomb next.
                        elif board[space] == "*":
                                for bomb in bomb_spaces: # Reveal all bombs on the board.
                                        display[bomb] = "*"
                                status = "Loss" # Lose the game. Ends loop.
                                displayBoard(display, status, bomb_ct, flag_ct) # Display game loss
                        # We will check if the space is the value 0.
                        elif board[space] == 0: # 0 is a special value because we...
                                propagate(space, display, board) # ...reveal the neighbor values.
                        # The space must be empty and a regular number. Reveal it!
                        else:
                                display[space] = board[space]
                                
                # CHECK WIN CONDITION
                remaining_space_check = 0
                for index in range(1, len(display)): # Compare all board spaces
                        if display[index] == ' ' or display[index] == 'F':
                                remaining_space_check += 1 # Increment remaining empty or flagged spaces.
                if remaining_space_check == bomb_ct: # When there are the same amount of empty or flagged spaces as bombs on the field...
                        status = "Victory!" # The game has been won! End game loop.
                        displayBoard(display, status, bomb_ct, flag_ct) # Display board one last time.
        return
main()
