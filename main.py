import tkinter as tk
from tkinter import messagebox


class Game:
    """Class representing the Tic Tac Toe game logic."""

    def __init__(self):
        """Initialize the game with an empty board and starting player."""

        self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.current_player = 1  # 1 for Player, 2 for AI

    def make_move(self, row, col):
        """Make a move on the board if the cell is empty."""

        if self.board[row][col] == 0:
            self.board[row][col] = self.current_player

            return True

        return False

    def switch_player(self):
        """Switch between Player and AI."""

        self.current_player = 3 - self.current_player  # Switch between player 1 and player 2

    def check_win(self, player):
        """Check if the specified player has won."""

        # Check rows and columns
        for i in range(3):
            if (self.board[i][0] == player and self.board[i][1] == player and self.board[i][2] == player) or \
                    (self.board[0][i] == player and self.board[1][i] == player and self.board[2][i] == player):
                return True

        # Check diagonals
        return (self.board[0][0] == player and self.board[1][1] == player and self.board[2][2] == player) or \
            (self.board[0][2] == player and self.board[1][1] == player and self.board[2][0] == player)

    def is_board_full(self):
        """Check if the board is full."""

        for row in self.board:
            for cell in row:
                if cell == 0:
                    return False

        return True

    def is_game_over(self):
        """Check if the game is over (win, draw, or still ongoing)."""

        return self.check_win(1) or self.check_win(2) or self.is_board_full()


class TicTacToeGUI:
    """Class representing the GUI for the Tic Tac Toe game."""

    def __init__(self, root):
        """Initialize the GUI with buttons and game logic."""

        self.root = root
        self.root.title("Tic Tac Toe")
        self.game = Game()

        # Create buttons
        self.buttons = [[None, None, None] for _ in range(3)]

        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(root, text="", font=('normal', 20), width=8, height=4,
                                               command=lambda row=i, col=j: self.on_button_click(row, col))
                self.buttons[i][j].grid(row=i, column=j)

    def on_button_click(self, row, col):
        """Handle button click events."""

        if not self.game.is_game_over() and self.game.make_move(row, col):
            self.update_button_text(row, col)

            if self.game.check_win(self.game.current_player):
                self.show_winner_message()

            elif self.game.is_board_full():
                self.show_draw_message()

            else:
                self.game.switch_player()
                self.ai_move()

    def ai_move(self):
        """Perform the AI's move."""

        if not self.game.is_game_over():
            best_move = self.get_best_move()

            self.game.make_move(best_move[0], best_move[1])

            self.update_button_text(best_move[0], best_move[1])

            if self.game.check_win(self.game.current_player):
                self.show_winner_message()

            elif self.game.is_board_full():
                self.show_draw_message()

            else:
                self.game.switch_player()

    def get_best_move(self):
        """Get the AI's best move using the minimax algorithm."""

        best_score = float('-inf')
        best_move = None

        for i in range(3):
            for j in range(3):
                if self.game.board[i][j] == 0:
                    self.game.make_move(i, j)
                    score = self.minimax(self.game.board, 0, False)
                    self.game.board[i][j] = 0
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)

        return best_move


    def minimax(self, board, depth, is_maximizing):
        """Implementation of the minimax algorithm."""

        if self.game.check_win(1):
            return -1

        elif self.game.check_win(2):
            return 1

        elif self.game.is_board_full():
            return 0

        if is_maximizing:
            max_eval = float('-inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == 0:
                        board[i][j] = 2
                        eval = self.minimax(board, depth + 1, False)
                        board[i][j] = 0
                        max_eval = max(max_eval, eval)

            return max_eval

        else:
            min_eval = float('inf')

            for i in range(3):
                for j in range(3):
                    if board[i][j] == 0:
                        board[i][j] = 1
                        eval = self.minimax(board, depth + 1, True)
                        board[i][j] = 0
                        min_eval = min(min_eval, eval)

            return min_eval

    def get_best_move2(self):
        """
        This function calculates the best move for the AI using the minimax algorithm with alpha-beta pruning.
        """
        best_score = float('-inf')
        best_move = None
        alpha = float('-inf')
        beta = float('inf')

        for i in range(3):
            for j in range(3):
                if self.game.board[i][j] == 0:
                    self.game.make_move(i, j)
                    score = self.minimax_alpha_beta(self.game.board, 0, False, alpha, beta)
                    self.game.board[i][j] = 0
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
                    alpha = max(alpha, best_score)

        return best_move

    def minimax_alpha_beta(self, board, depth, is_maximizing, alpha, beta):
        """
        This function implements the minimax algorithm with alpha-beta pruning for selecting the best move by the AI.
        """
        if self.game.check_win(1):
            return -1
        elif self.game.check_win(2):
            return 1
        elif self.game.is_board_full():
            return 0

        if is_maximizing:
            max_eval = float('-inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == 0:
                        board[i][j] = 2
                        eval = self.minimax_alpha_beta(board, depth + 1, False, alpha, beta)
                        board[i][j] = 0
                        max_eval = max(max_eval, eval)
                        alpha = max(alpha, eval)
                        if beta <= alpha:
                            break  # Smart pruning the loop
            return max_eval
        else:
            min_eval = float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == 0:
                        board[i][j] = 1
                        eval = self.minimax_alpha_beta(board, depth + 1, True, alpha, beta)
                        board[i][j] = 0
                        min_eval = min(min_eval, eval)
                        beta = min(beta, eval)
                        if beta <= alpha:
                            break  # Smart pruning the loop
            return min_eval

    def update_button_text(self, row, col):
        """Update the text on the clicked button with the current player's symbol."""

        player_symbol = "X" if self.game.current_player == 1 else "O"
        self.buttons[row][col].config(text=player_symbol, state=tk.DISABLED)

    def show_winner_message(self):
        """Display a message box with the winner."""

        winner = "Player" if self.game.current_player == 1 else "AI"
        messagebox.showinfo("Game Over", f"{winner} wins!")

    @staticmethod
    def show_draw_message():
        """Display a message box for a draw."""

        messagebox.showinfo("Game Over", "It's a draw!")


if __name__ == "__main__":
    while True:
        root = tk.Tk()
        app = TicTacToeGUI(root)
        root.mainloop()
