import random
class Cell:
        def __init__(self):
                self.adjMines = 0
                self.covered = True
                self.bomb = False
                self.flagged = False

        def __str__(self):
                #for debugging
                #if self.bomb:
                        #return 'BOOM'

                if self.flagged:
                        return 'F'
                elif self.covered:
                        return ' '
                else:
                        return str(self.adjMines)


class Board:
        def __init__(self):
                self._board = []
                for i in range(1, 102):
                        self._board.append(Cell())

        def __getitem__(self, i):  # OVERLOAD INDEXING
                if isinstance(i, int):
                        return self._board[i]
                else:
                        raise
        
        def __len__(self):
                return len(self._board)
        
        def display(self): # FUNCTION TO DISPLAY USER'S BOARD
                print('\n    A  B  C  D  E  F  G  H  I  J  ')

                test_string = ''
                for i in range(10):
                        for j in range(10):
                                test_string += '[' + str(self._board[(((i*10)+j)+1)]) +']'
                        if (i+1 != 10): # Prints rows with built string above.
                                print(str(i+1) + '  ' + test_string)
                        else: # Row 10 requires less space between itself and test string.
                                print(str(i+1) + ' ' + test_string)
                        test_string = '' # Empty test string.
                return

        def getNeighbors(self, num): # Helps narrow the spaces to check bombs for a given space
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




        
class Game:
        def __init__(self):
                self.status = 'Playing'
                self.flag_ct = 0
                self.bomb_ct = 0
                self.first_click = False
                self.bomb_spaces = []
                self.board = Board()

        def printGame(self):
                self.board.display()
                print("Current status:", self.status)
                print("Mines remaining:", self.bomb_ct - self.flag_ct, "\n")
                return

        def placeBombs(self): # Translates to old generateBoard(). NEEDS TESTING.
                for i in range(len(self.bomb_spaces)):
                        bomb_idx = self.bomb_spaces[i] # Get location of bomb
                        self.board[bomb_idx].bomb = True # Insert bomb character

                # Now we just need to fill values around bombs!

                for i in range(1, len(self.board)): # For every space in the board we need to find how many bombs are around it.
                        if (self.board[i].bomb):
                                continue # We don't need the value where bombs are so we skip.
                        space_val = 0
                        neighbors = self.board.getNeighbors(i) # We'll get the valid indices in separate function.
                        for index in neighbors: # Iterate through neighbor list
                                if (self.board[index].bomb): # If the board at that neighbor is a bomb...
                                        space_val += 1 # ...increment space value
                        self.board[i].adjMines = space_val # Set value at that board space.

        def propagate(self, space):
                self.board[space].covered = False
                neighbors = self.board.getNeighbors(space)
                for neighbor in neighbors:
                        if self.board[neighbor].adjMines == 0 and self.board[neighbor].flagged == False:
                                if self.board[neighbor].covered:
                                        self.propagate(neighbor)
                        elif self.board[neighbor].flagged:
                                continue
                        else:
                                print(f"Cell {neighbor}")
                                self.board[neighbor].covered = False

        def getInput(self): # Parses given command into usable interpretation for program.
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

        def play(self):
                # COLLECT BOMB AMOUNT (DIFFICULTY)
                i = 0
                while i == 0: # This while loop is purely for error handling. We don't stop asking until we get workable input!
                        try:
                                self.bomb_ct = int(input('How many bombs should there be?: '))
                                if self.bomb_ct < 10 or self.bomb_ct > 20: # Bomb count must be between 10 and 20 per the requirements.
                                        raise
                                i = 1
                        except:
                                print("Invalid bomb count. Please input again.")

                self.printGame()


newgame = Game()
newgame.bomb_spaces = [1,2,3,4,5,6,7,8,9,10]
newgame.placeBombs()
newgame.printGame()

newgame.propagate(100)
newgame.printGame()




        

