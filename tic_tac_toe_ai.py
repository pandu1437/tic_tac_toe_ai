import tkinter as tk
from tkinter import messagebox

# Constants for players
HUMAN = 'X'
AI = 'O'

class TicTacToeAI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe with AI (Minimax)")
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.create_buttons()
        self.game_over = False

    def create_buttons(self):
        frame = tk.Frame(self.root)
        frame.pack()
        for i in range(3):
            for j in range(3):
                btn = tk.Button(frame, text='', font=('Arial', 40), width=5, height=2,
                                command=lambda r=i, c=j: self.human_move(r, c))
                btn.grid(row=i, column=j)
                self.buttons[i][j] = btn
        reset_btn = tk.Button(self.root, text='Reset', font=('Arial', 14), command=self.reset_game)
        reset_btn.pack(pady=10)

    def human_move(self, row, col):
        if self.game_over or self.board[row][col] != '':
            return
        self.board[row][col] = HUMAN
        self.buttons[row][col].config(text=HUMAN, state='disabled')
        if self.check_winner(self.board, HUMAN):
            self.game_over = True
            messagebox.showinfo("Game Over", "You Win!")
        elif self.is_draw(self.board):
            self.game_over = True
            messagebox.showinfo("Game Over", "It's a Draw!")
        else:
            self.root.after(200, self.ai_move)

    def ai_move(self):
        if self.game_over:
            return
        move = self.best_move()
        if move:
            row, col = move
            self.board[row][col] = AI
            self.buttons[row][col].config(text=AI, state='disabled')
            if self.check_winner(self.board, AI):
                self.game_over = True
                messagebox.showinfo("Game Over", "AI Wins!")
            elif self.is_draw(self.board):
                self.game_over = True
                messagebox.showinfo("Game Over", "It's a Draw!")

    def best_move(self):
        best_score = float('-inf')
        move = None
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == '':
                    self.board[i][j] = AI
                    score = self.minimax(self.board, 0, False)
                    self.board[i][j] = ''
                    if score > best_score:
                        best_score = score
                        move = (i, j)
        return move

    def minimax(self, board, depth, is_maximizing):
        if self.check_winner(board, AI):
            return 10 - depth
        elif self.check_winner(board, HUMAN):
            return depth - 10
        elif self.is_draw(board):
            return 0

        if is_maximizing:
            best_score = float('-inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == '':
                        board[i][j] = AI
                        score = self.minimax(board, depth + 1, False)
                        board[i][j] = ''
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == '':
                        board[i][j] = HUMAN
                        score = self.minimax(board, depth + 1, True)
                        board[i][j] = ''
                        best_score = min(score, best_score)
            return best_score

    def check_winner(self, board, player):
        # Rows, columns and diagonals
        for i in range(3):
            if all(board[i][j] == player for j in range(3)):
                return True
            if all(board[j][i] == player for j in range(3)):
                return True
        if board[0][0] == board[1][1] == board[2][2] == player:
            return True
        if board[0][2] == board[1][1] == board[2][0] == player:
            return True
        return False

    def is_draw(self, board):
        return all(board[i][j] != '' for i in range(3) for j in range(3))

    def reset_game(self):
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.game_over = False
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text='', state='normal')

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToeAI(root)
    root.mainloop()
