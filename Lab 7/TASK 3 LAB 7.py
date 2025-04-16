import random

size = 10
ship_lengths = [3]

def new_board():
    return [["~" for _ in range(size)] for _ in range(size)]

def show_board(board, reveal=False):
    print("  " + " ".join([chr(ord('A') + i) for i in range(size)]))
    for i, row in enumerate(board):
        line = f"{i} " + " ".join(row if reveal else ['~' if cell == 'S' else cell for cell in row])
        print(line)

def add_ship(board, length):
    done = False
    while not done:
        x = random.randint(0, size - 1)
        y = random.randint(0, size - 1)
        dir = random.choice(["H", "V"])
        if dir == "H" and y + length <= size:
            if all(board[x][y+i] == "~" for i in range(length)):
                for i in range(length):
                    board[x][y+i] = "S"
                done = True
        elif dir == "V" and x + length <= size:
            if all(board[x+i][y] == "~" for i in range(length)):
                for i in range(length):
                    board[x+i][y] = "S"
                done = True

def parse_input(text):
    try:
        col = ord(text[0].upper()) - ord('A')
        row = int(text[1:])
        if 0 <= col < size and 0 <= row < size:
            return row, col
    except:
        return None
    return None

def ai_choice(used):
    while True:
        r = random.randint(0, size - 1)
        c = random.randint(0, size - 1)
        if (r, c) not in used:
            return r, c

def is_sunk(board, r, c):
    for dx in [-1, 1]:
        i = r + dx
        while 0 <= i < size and board[i][c] in ("S", "X"):
            if board[i][c] == "S":
                return False
            i += dx
    for dy in [-1, 1]:
        j = c + dy
        while 0 <= j < size and board[r][j] in ("S", "X"):
            if board[r][j] == "S":
                return False
            j += dy
    return True

def game_over(board):
    return all(cell != "S" for row in board for cell in row)

player = new_board()
ai = new_board()
for l in ship_lengths:
    add_ship(player, l)
    add_ship(ai, l)

ai_moves = set()

while True:
    print("\nYour Turn")
    show_board(ai)
    move = input("Enter your attack (e.g., B4): ").strip()
    pos = parse_input(move)
    if not pos:
        print("Invalid input. Try again.")
        continue

    x, y = pos
    if ai[x][y] == "S":
        ai[x][y] = "X"
        if is_sunk(ai, x, y):
            print(f"Player attacks: {move.upper()} → Sunk!")
        else:
            print(f"Player attacks: {move.upper()} → Hit!")
    elif ai[x][y] in ("X", "O"):
        print("Already attacked here.")
        continue
    else:
        ai[x][y] = "O"
        print(f"Player attacks: {move.upper()} → Miss")

    if game_over(ai):
        print("You win! All enemy ships sunk.")
        break

    print("\nAI's Turn")
    ax, ay = ai_choice(ai_moves)
    ai_moves.add((ax, ay))

    if player[ax][ay] == "S":
        player[ax][ay] = "X"
        if is_sunk(player, ax, ay):
            print(f"AI attacks: {chr(ay + ord('A'))}{ax} → Sunk!")
        else:
            print(f"AI attacks: {chr(ay + ord('A'))}{ax} → Hit!")
    else:
        player[ax][ay] = "O"
        print(f"AI attacks: {chr(ay + ord('A'))}{ax} → Miss")

    if game_over(player):
        print("AI wins! All your ships are sunk.")
        break
