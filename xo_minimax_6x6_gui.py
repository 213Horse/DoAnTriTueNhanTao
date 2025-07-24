import math
import random
import tkinter as tk
from tkinter import messagebox

BOARD_SIZE = 6
WIN_CONDITION = 5
PLAYER = 'X'
AI = 'O'
MAX_DEPTH = 3  # Giới hạn độ sâu để tránh chậm khi board quá lớn

# Tạo bảng trắng
def create_board():
    return [[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

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

# Giao diện Tkinter
class XOGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Caro 6x6 vs AI")
        self.board = create_board()
        self.buttons = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.create_widgets()
        self.game_over = False
        self.waiting_for_ai = False  # Thêm biến này

    def create_widgets(self):
        frame = tk.Frame(self.root)
        frame.pack()
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                btn = tk.Button(frame, text=' ', width=4, height=2, font=('Arial', 20),
                                command=lambda r=r, c=c: self.player_move(r, c))
                btn.grid(row=r, column=c)
                self.buttons[r][c] = btn
        self.reset_btn = tk.Button(self.root, text="Chơi lại", command=self.reset_game)
        self.reset_btn.pack(pady=10)

    def player_move(self, r, c):
        if self.game_over or self.waiting_for_ai or self.board[r][c] != ' ':
            return
        self.board[r][c] = PLAYER
        self.buttons[r][c]['text'] = PLAYER
        self.buttons[r][c]['state'] = 'disabled'
        if check_win(self.board, PLAYER):
            self.end_game("Bạn thắng!")
            return
        elif not get_available_moves(self.board):
            self.end_game("Hòa!")
            return
        self.waiting_for_ai = True
        self.disable_all_buttons()
        self.root.after(300, self.ai_move)

    def ai_move(self):
        if self.game_over:
            return
        _, move = minimax(self.board, MAX_DEPTH, True)
        if move:
            r, c = move
            self.board[r][c] = AI
            self.buttons[r][c]['text'] = AI
            self.buttons[r][c]['state'] = 'disabled'
        if check_win(self.board, AI):
            self.end_game("AI thắng!")
        elif not get_available_moves(self.board):
            self.end_game("Hòa!")
        else:
            self.waiting_for_ai = False
            self.enable_empty_buttons()

    def disable_all_buttons(self):
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                self.buttons[r][c]['state'] = 'disabled'

    def enable_empty_buttons(self):
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if self.board[r][c] == ' ':
                    self.buttons[r][c]['state'] = 'normal'

    def end_game(self, message):
        self.game_over = True
        self.waiting_for_ai = False
        messagebox.showinfo("Kết thúc", message)
        self.disable_all_buttons()

    def reset_game(self):
        self.board = create_board()
        self.game_over = False
        self.waiting_for_ai = False
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                self.buttons[r][c]['text'] = ' '
                self.buttons[r][c]['state'] = 'normal'

if __name__ == "__main__":
    root = tk.Tk()
    game = XOGameGUI(root)
    root.mainloop() 