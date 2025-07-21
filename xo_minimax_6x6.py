import math
import random

BOARD_SIZE = 6
WIN_CONDITION = 5
PLAYER = 'X'
AI = 'O'
MAX_DEPTH = 3  # Giới hạn độ sâu để tránh chậm khi board quá lớn

# Tạo bảng trắng
def create_board():
    return [[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

# In ra bàn cờ
def print_board(board):
    print("  " + " ".join(str(i) for i in range(BOARD_SIZE)))
    for idx, row in enumerate(board):
        print(f"{idx} " + " ".join(row))

# Kiểm tra ô trống
def get_available_moves(board):
    return [(r, c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE) if board[r][c] == ' ']

# Kiểm tra thắng
def check_win(board, player):
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if (c + WIN_CONDITION <= BOARD_SIZE and all(board[r][c + i] == player for i in range(WIN_CONDITION))) or \
               (r + WIN_CONDITION <= BOARD_SIZE and all(board[r + i][c] == player for i in range(WIN_CONDITION))) or \
               (r + WIN_CONDITION <= BOARD_SIZE and c + WIN_CONDITION <= BOARD_SIZE and all(board[r + i][c + i] == player for i in range(WIN_CONDITION))) or \
               (r - WIN_CONDITION + 1 >= 0 and c + WIN_CONDITION <= BOARD_SIZE and all(board[r - i][c + i] == player for i in range(WIN_CONDITION))):
                return True
    return False

# Kiểm tra kết thúc
def is_terminal(board):
    return check_win(board, PLAYER) or check_win(board, AI) or not get_available_moves(board)

# Hàm đánh giá đơn giản
def evaluate(board):
    if check_win(board, AI): return 10
    elif check_win(board, PLAYER): return -10
    else: return 0

# Giải thuật minimax
def minimax(board, depth, is_maximizing):
    if is_terminal(board) or depth == 0:
        return evaluate(board), None

    best_move = None
    if is_maximizing:
        max_eval = -math.inf
        for move in get_available_moves(board):
            r, c = move
            board[r][c] = AI
            eval, _ = minimax(board, depth - 1, False)
            board[r][c] = ' '
            if eval > max_eval:
                max_eval = eval
                best_move = move
        return max_eval, best_move
    else:
        min_eval = math.inf
        for move in get_available_moves(board):
            r, c = move
            board[r][c] = PLAYER
            eval, _ = minimax(board, depth - 1, True)
            board[r][c] = ' '
            if eval < min_eval:
                min_eval = eval
                best_move = move
        return min_eval, best_move

# Chương trình chính
def play_game():
    board = create_board()
    print("Welcome to 6x6 XO Game vs AI!")
    print_board(board)

    while not is_terminal(board):
        # Người chơi
        while True:
            try:
                row = int(input("Nhập hàng (0-5): "))
                col = int(input("Nhập cột (0-5): "))
                if board[row][col] == ' ':
                    board[row][col] = PLAYER
                    break
                else:
                    print("Ô đã có người chọn!")
            except:
                print("Nhập không hợp lệ!")
        print_board(board)

        if check_win(board, PLAYER):
            print("Bạn thắng!")
            return
        elif not get_available_moves(board):
            print("Hòa!")
            return

        # AI
        print("AI đang suy nghĩ...")
        _, move = minimax(board, MAX_DEPTH, True)
        if move:
            r, c = move
            board[r][c] = AI
            print(f"AI chọn: ({r}, {c})")
            print_board(board)

        if check_win(board, AI):
            print("AI thắng!")
            return
        elif not get_available_moves(board):
            print("Hòa!")
            return

# Chạy chương trình
if __name__ == "__main__":
    play_game()