import random

BOMB = "💣"
FLAG = "🚩"

def choosePlayerProfile():
    print("Available profiles:")
    import os
    profiles = [f.replace(".txt", "") for f in os.listdir() if f.endswith(".txt")]
    if profiles:
        for i, p in enumerate(profiles, 1):
            print(f"{i}. {p}")
    else:
        print("No profiles found.")

    while True:
        choice = input("Enter profile name to use (or new name to create): ").strip()
        if choice:
            return choice


def savePlayerData(player_name, data):
    with open(f"{player_name}.txt", "w", encoding="utf-8") as f:
        for key, value in data.items():
            f.write(f"{key}:{value}\n")


def loadPlayerData(player_name):
    data = {}
    try:
        with open(f"{player_name}.txt", "r", encoding="utf-8") as f:
            for line in f:
                key, value = line.strip().split(":", 1)
                data[key] = value
    except FileNotFoundError:
        pass
    return data


def getNeighbors(num):  # Helps narrow the spaces to check bombs for a given space
    isLeftEdge = False
    isRightEdge = False
    if ((num - 1) % 10) == 0:
        isLeftEdge = True
    if (num % 10) == 0:
        isRightEdge = True
    neighbors = []
    if not isRightEdge:
        neighbors.append(num + 1)
    if not isLeftEdge:
        neighbors.append(num - 1)
    if (num + 10 < 101):
        neighbors.append(num + 10)
    if (num - 10 > 0):
        neighbors.append(num - 10)
    if (not isLeftEdge) and (num - 10 > 0):
        neighbors.append(num - 11)
    if (not isRightEdge) and (num - 10 > 0):
        neighbors.append(num - 9)
    if (not isLeftEdge) and (num + 10 < 101):
        neighbors.append(num + 9)
    if (not isRightEdge) and (num + 10 < 101):
        neighbors.append(num + 11)
    return neighbors


def propagate(space, display, board):
    display[space] = board[space]
    neighbors = getNeighbors(space)
    for neighbor in neighbors:
        if board[neighbor] == 0 and display[neighbor] != FLAG:
            if display[neighbor] != 0:
                propagate(neighbor, display, board)
        elif display[neighbor] == FLAG:
            continue
        else:
            display[neighbor] = board[neighbor]


def generateBoard(bomb_spaces):
    board = []
    for i in range(1, 102):
        board.append(0)
    for i in range(len(bomb_spaces)):
        bomb_idx = bomb_spaces[i]
        board[bomb_idx] = BOMB

    for i in range(1, len(board)):
        if (board[i] == BOMB):
            continue
        space_val = 0
        neighbors = getNeighbors(i)
        for index in neighbors:
            if (board[index] == BOMB):
                space_val += 1
        board[i] = space_val
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


def displayBoard(display, status, bomb_ct, flag_ct):
    print('\n    A  B  C  D  E  F  G  H  I  J  ')
    test_string = ''
    for i in range(10):
        for j in range(10):
            test_string += '[' + str(display[(((i * 10) + j) + 1)]) + ']'
        if (i + 1 != 10):
            print(str(i + 1) + '  ' + test_string)
        else:
            print(str(i + 1) + ' ' + test_string)
        test_string = ''
    print("Current status:", status)
    print("Mines remaining:", bomb_ct - flag_ct, "\n")
    return


def getInput():
    i = True
    while i:
        try:
            inp_string = input('Please give command: ')
            com_type = inp_string[0].lower()
            if com_type not in ["m", "f", "q"]:
                raise
            if com_type == "q":
                return [com_type]
            inp_string = inp_string[1:len(inp_string)]
            col = inp_string[len(inp_string) - 1]
            cols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
            if col not in cols:
                raise
            col = cols.index(col) + 1
            inp_string = inp_string[:len(inp_string) - 1]
            row = int(inp_string)
            if row not in range(1, 11):
                raise
            i = False
        except:
            print('\nCommand is faulty please follow command, row, column format.')
            print('(Hint 1: To mine at row 1, column a, type "m1a")')
            print('(Hint 2: To flag at row 7, column g, type "f7g")\n')
            continue

    command = []
    command.append(com_type)
    command.append(row)
    command.append(col)

    return command


def minereveal(display, bomb_spaces):
    for bomb in bomb_spaces:
        display[bomb] = BOMB

def main():
    player_name = choosePlayerProfile()
    player_data = loadPlayerData(player_name)
    print(f"Welcome {player_name}!")
    if player_data:
        print("Resuming previous game if exists.")
    else:
        print("No previous data found. Starting fresh!")

    # Load previous game state if available
    bomb_ct = int(player_data.get("bomb_count", "10"))

    bomb_spaces_str = player_data.get("bomb_spaces", "")
    if bomb_spaces_str:
        bomb_spaces = [int(b) for b in bomb_spaces_str.split(',')]
    else:
        bomb_spaces = random.sample(range(1, 101), bomb_ct)

    display_str = player_data.get("display", "")
    display = [' ']  # index 0 placeholder
    if display_str:
        display += display_str.split(',')
    else:
        display += [' '] * 100

    flag_ct = int(player_data.get("flag_ct", "0"))
    status = player_data.get("status", "Playing")

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
    print('- Type "q" to quit and save the game.')
    print('- Win by uncovering every safe space. If you hit a mine, you lose!.')
    print('--------------------------------')

    if not bomb_spaces_str:
        i = 0
        while i == 0:
            try:
                bomb_ct = int(input('How many bombs should there be?: '))
                if bomb_ct < 10 or bomb_ct > 20:
                    raise
                i = 1
            except:
                print("Invalid bomb count. Please input again.")

    displayBoard(display, status, bomb_ct, flag_ct)

    # If no previous game, generate board
    board = generateBoard(bomb_spaces)

    while status == "Playing":
        displayBoard(display, status, bomb_ct, flag_ct)
        user_input = getInput()
        if user_input[0] == "q":
            # Save game state and exit
            player_data["bomb_spaces"] = ','.join(str(b) for b in bomb_spaces)
            player_data["display"] = ','.join(str(x) for x in display[1:])  # skip index 0
            player_data["flag_ct"] = str(flag_ct)
            player_data["status"] = status
            savePlayerData(player_name, player_data)
            print("Game saved. You can resume later!")
            return

        space = ((user_input[1] - 1) * 10) + user_input[2]

        if user_input[0] == 'f':
            if display[space] == ' ':
                if flag_ct + 1 > bomb_ct:
                    print("Cannot flag any more spaces. Please unflag with flag command.")
                else:
                    display[space] = FLAG
                    flag_ct += 1
            elif display[space] == FLAG:
                display[space] = ' '
                flag_ct -= 1
            else:
                print("Cannot flag given space.")

        elif user_input[0] == 'm':
            if display[space] == FLAG:
                print("Cannot mine here. Flag is in the way.")
            elif board[space] == BOMB:
                minereveal(display, bomb_spaces)
                status = "Game Over"
                displayBoard(display, status, bomb_ct, flag_ct)
                print("\nYou Hit a Mine! Game Over. \n")
            elif board[space] == 0:
                propagate(space, display, board)
            else:
                display[space] = board[space]

        remaining_space_check = 0
        for index in range(1, len(display)):
            if display[index] == ' ' or display[index] == FLAG:
                remaining_space_check += 1
        if remaining_space_check == bomb_ct:
            status = "Victory!"
            displayBoard(display, status, bomb_ct, flag_ct)
            print("\n Congratulations! You Won! \n")
            break

        # Autosave after each turn
        player_data["bomb_spaces"] = ','.join(str(b) for b in bomb_spaces)  # store bomb positions
        player_data["display"] = ','.join(str(x) for x in display[1:])  # store display board
        player_data["flag_ct"] = str(flag_ct)
        player_data["status"] = status
        savePlayerData(player_name, player_data)

    return


main()
