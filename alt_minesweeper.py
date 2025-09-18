import random
import os

class Cell:
        def __init__(self):
                self.adjMines = 0
                self.covered = True
                self.bomb = False
                self.flagged = False

        def __str__(self):
                #for debugging
                if self.bomb and not self.covered:
                        return "💣"
                if self.flagged:
                        return "🚩"
                elif self.covered:
                        return '  '
                else:
                        return f" {str(self.adjMines)}"


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
                print('     A   B   C   D   E   F   G   H   I   J  ')

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
                                #print(f"Cell {neighbor}")
                                self.board[neighbor].covered = False

        def printErr(self, msg):
                print(msg)
                input("Press [ENTER] to continue...")

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
                                err_msg = '\nCommand is faulty please follow command, row, column format.\n(Hint 1: To mine at row 1, column a, type "m1a")\n(Hint 2: To flag at row 7, column g, type "f7g")'
                                self.printErr(err_msg)
                                continue
                
                command = [] # Create command value.
                command.append(com_type) # Add the "m" or "f"
                command.append(row) # Add row number.
                command.append(col) # Add column number.
                return command # Return parsed input.



        def configure(self):
                # COLLECT BOMB AMOUNT (DIFFICTULTY)
                i = 0
                while i == 0: # This while loop is purely for error handling. We don't stop asking until we get workable input!
                        try:
                                self.bomb_ct = int(input('How many bombs should there be?: '))
                                if self.bomb_ct < 10 or self.bomb_ct > 20: # Bomb count must be between 10 and 20 per the requirements.
                                        raise
                                i = 1
                        except:
                                print("Invalid bomb count. Please input again.")
                self.bomb_spaces = random.sample(range(1,101), self.bomb_ct)




        def move(self, prebomb=False):
                user_input = self.getInput() # Helper function gives us actionable command.
                space = ((user_input[1]-1)*10) + user_input[2] # Translate col and row from input into board space.
                
                if user_input[0] == 'f': # If we got a flag command, we place the flag on display.
                        if not self.board[space].flagged: # Empty space means flag is allowed.
                                        if self.flag_ct + 1 > self.bomb_ct: # Also got to check that we don't place too many flags.
                                                self.printErr("Cannot flag any more spaces. Please unflag with flag command.")
                                        elif not self.board[space].covered:
                                                self.printErr("Cannot flag an uncovered space.")
                                        else:
                                                self.board[space].flagged = True # Put a flag on the display!
                                                self.flag_ct += 1 # Increment the amount of flags on board.
                        elif self.board[space].flagged: # Flag exists in current space, remove it.
                                self.board[space].flagged = False # Set flag to empty space.
                                self.flag_ct -= 1 # Decrement the amount of flags on board.
                
                elif user_input[0] == 'm': # We have a mine command!
                        if self.board[space].flagged: # Are we mining on a flag space?
                                self.printErr('Cannot mine a flagg given space.') # We don't actually do anything. We just say a flag is in the way.
                        else:
                                if prebomb:
                                        # SPACE-BOMB COLLISION PROBLEM
                                        if space in self.bomb_spaces: # In the event the selected space is where a mine was planned to be...
                                                problem_index = self.bomb_spaces.index(space) # Isolate where in the list of bomb spaces the user space and bomb collide.
                                                while space == self.bomb_spaces[problem_index]: # While these two values are the same...
                                                        self.bomb_spaces[problem_index] = random.randint(1, 100) # ...we will reroll that bomb space.
                                                        i = 0 # Then we'll check how many times the new bomb space value appears.
                                                        for place in self.bomb_spaces: # Check every bomb space
                                                                if self.bomb_spaces[problem_index] == place: # If the new space appears in bomb spaces, increment.
                                                                        i += 1 # This should increment only once (when the new space compares itself).
                                                        if i > 1: # If the new bomb space increments multiple times, we still have a collision.
                                                                self.bomb_spaces[problem_index] = space # We can't let the while loop end so reset with space.
                                        
                                        # CALL BOARD GENERATION
                                        self.placeBombs()
                                        # UPDATE BOARD w/ FIRST SPACE
                                        if self.board[space].adjMines == 0:
                                                self.propagate(space) # Reveal spaces around the 0 space.
                                        else:
                                                self.board[space].covered = False
                                else:
                                        # There's a few things we check here:
                                                # Is the space a bomb?
                                                # Is the space a flag?
                                                # Is the space 0?
                                                # Is the space any other value?
                                        # We will check if the space is a bomb next.
                                        if self.board[space].bomb:
                                                for bomb in self.bomb_spaces: # Reveal all bombs on the board.
                                                        self.board[bomb].covered = False
                                                self.status = "Loss" # Lose the game.
                                        # We will check if the space is the value 0.
                                        elif self.board[space].adjMines == 0: # 0 is a special value because we...
                                                self.propagate(space) # ...reveal the neighbor values.
                                        # The space must be empty and a regular number. Reveal it!
                                        else:
                                                self.board[space].covered = False

        def checkWin(self):
                # CHECK WIN CONDITION
                remaining_space_check = 0
                for index in range(1, len(self.board)): # Compare all board spaces
                        if self.board[index].covered:
                                remaining_space_check += 1 # Increment remaining empty or flagged spaces.
                if remaining_space_check == self.bomb_ct: # When there are the same amount of empty or flagged spaces as bombs on the field...
                        status = "Victory!" # The game has been won! End game loop.

        def checkBombPlacement(self):
                bombed_spaces = 0
                for index in range(1, len(self.board)):
                        if self.board[index].bomb:
                                bombed_spaces += 1
                return bombed_spaces == self.bomb_ct


        def play(self):
                self.configure()
                while not self.checkBombPlacement():
                        self.printGame()
                        #print(f"Bomb Spaces: {self.bomb_spaces}")
                        self.move(True)
                        os.system('clear')
                while self.status == 'Playing':
                        self.printGame()
                        #print(f"Bomb Spaces: {self.bomb_spaces}")
                        self.move()
                        self.checkWin()
                        os.system('clear')
                self.printGame()
                return




class GameManager:
        def __init__(self):
                return
        
        def newGame(self):
                newgame = Game()
                newgame.play()
        
        def start_message(self):
                print('Welcome to Minesweeper!')
                print('--------------------------------')
                print('HOW TO PLAY:')
                print('- Goal: uncover all safe spaces without hitting a mine.')
                print('- The numbers show how many mines are in the surrounding spaces.')
                print('- Commands (one command per turn):')
                print('    m[row][col] → Uncover a space.')
                print('        Example: m3b means uncover row 3, column b.')
                print('    f[row][col] → Flag or unflag a space.')
                print('        Example: f5h means place/remove a flag at row 5, column h.')
                #print('- Type "q" to quit and save the game.')
                print('- Win by uncovering every safe space. If you hit a mine, you lose!.')
                print('--------------------------------')
        
        def start(self):
                self.start_message()
                while True:
                        self.newGame()
                        choice = input("Play again?(yes/no): ")
                        if choice == 'yes':
                                os.system('clear')
                                continue
                        else:
                                break

def main():
        manager = GameManager()
        manager.start()

main()