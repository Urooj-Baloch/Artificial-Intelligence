import copy

EMPTY = '.'
WHITE = 'W'
BLACK = 'B'

BOARD_SIZE = 8

def create_board():
    board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    for row in range(3):
        for col in range(BOARD_SIZE):
            if (row + col) % 2 == 1:
                board[row][col] = BLACK
    for row in range(5, 8):
        for col in range(BOARD_SIZE):
            if (row + col) % 2 == 1:
                board[row][col] = WHITE
    return board

def print_board(board):
    print("   " + " ".join(str(c) for c in range(BOARD_SIZE)))
    for i, row in enumerate(board):
        print(f"{i}  " + " ".join(row))
    print()

def is_valid_move(board, start, end, player):
    r1, c1 = start
    r2, c2 = end
    if not (0 <= r2 < BOARD_SIZE and 0 <= c2 < BOARD_SIZE):
        return False
    if board[r2][c2] != EMPTY:
        return False
    dr = r2 - r1
    dc = abs(c2 - c1)
    if player == WHITE and dr == 1 and dc == 1:
        return True
    if player == BLACK and dr == -1 and dc == 1:
        return True
    return False

def make_move(board, start, end):
    r1, c1 = start
    r2, c2 = end
    player = board[r1][c1]
    board[r1][c1] = EMPTY
    board[r2][c2] = player

   
    if abs(r2 - r1) == 2:
        captured_r = (r1 + r2) // 2
        captured_c = (c1 + c2) // 2
        board[captured_r][captured_c] = EMPTY
        return True  
    return False

def get_all_moves(board, player):
    moves = []
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] == player:
                directions = [(-1, -1), (-1, 1)] if player == BLACK else [(1, -1), (1, 1)]
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and board[nr][nc] == EMPTY:
                        moves.append(((r, c), (nr, nc)))
             
                    cr, cc = r + 2 * dr, c + 2 * dc
                    if (0 <= cr < BOARD_SIZE and 0 <= cc < BOARD_SIZE and
                        board[r + dr][c + dc] not in (EMPTY, player) and
                        board[cr][cc] == EMPTY):
                        moves.append(((r, c), (cr, cc)))
    return moves

def minimax(board, depth, maximizing_player, alpha, beta):
   
    current_player = BLACK if maximizing_player else WHITE
    moves = get_all_moves(board, current_player)
    if not moves or depth == 0:
        return None, 0  
    best_move = moves[0]
    return best_move, 0

def play_game():
    board = create_board()
    print_board(board)
    
    while True:
     
        while True:
            try:
                move = input("Enter your move (e.g. 5 0 4 1): ")
                r1, c1, r2, c2 = map(int, move.strip().split())
                if board[r1][c1] != WHITE:
                    print("You must move a white piece!")
                    continue
                if not is_valid_move(board, (r1, c1), (r2, c2), WHITE):
                    print("Invalid move, try again.")
                    continue
                captured = make_move(board, (r1, c1), (r2, c2))
                print(f"Player moves: ({r1},{c1}) → ({r2},{c2}){' [Capture!]' if captured else ''}")
                break
            except:
                print("Invalid input. Try again.")
        
        print_board(board)

        ai_moves = get_all_moves(board, BLACK)
        if not ai_moves:
            print("AI has no moves. You win!")
            break

        ai_move, _ = minimax(board, 3, True, float('-inf'), float('inf'))
        if ai_move:
            (r1, c1), (r2, c2) = ai_move
            captured = make_move(board, (r1, c1), (r2, c2))
            print(f"AI moves: ({r1},{c1}) → ({r2},{c2}){' [Capture!]' if captured else ''}")
            print_board(board)
        else:
            print("No valid moves for AI. You win!")
            break

        if not get_all_moves(board, WHITE):
            print("You have no legal moves left. AI wins!")
            break

play_game()
