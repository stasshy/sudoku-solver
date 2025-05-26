import tkinter as tk
from tkinter import messagebox

class SudokuSolverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SUDOKU SOLVER")
        self.root.geometry("526x743")
        self.root.configure(bg="#91abc6")
        self.root.resizable(True, True)

        self.option_var = tk.StringVar()
        self.option_var.set("A")  # Set the default option to A

        self.label = tk.Label(root, text="Choose an option and click START:", font=("TkTextFont", 18), bg="#91abc6")
        self.label.place(x=0, y=50, width=526)

        self.radio_a = tk.Radiobutton(root, text="A: Enter your own Sudoku", variable=self.option_var, value="A", font=("TkTextFont", 14))
        self.radio_a.place(x=150, y=100)

        self.radio_b = tk.Radiobutton(root, text="B: Select an unsolved Sudoku", variable=self.option_var, value="B", font=("TkTextFont", 14))
        self.radio_b.place(x=150, y=130)

        self.start_button = tk.Button(root, command=self.start_solver, text="START", width=10, font=("TkTextFont", 14))
        self.start_button.place(x=150, y=200)

        self.exit_button = tk.Button(root, command=root.destroy, text="EXIT", width=10, font=("TkTextFont", 14))
        self.exit_button.place(x=275, y=200)

        self.difficulty_label = tk.Label(root, text="Select Difficulty:", font=("TkTextFont", 14), bg="#91abc6")
        self.easy_button = tk.Button(root, command=self.start_option_b_easy, text="Easy", width=10, font=("TkTextFont", 14))
        self.medium_button = tk.Button(root, command=self.start_option_b_medium, text="Medium", width=10, font=("TkTextFont", 14))
        self.hard_button = tk.Button(root, command=self.start_option_b_hard, text="Hard", width=10, font=("TkTextFont", 14))

    def start_solver(self):
        option = self.option_var.get()
        if option == "A":
            self.start_option_a()
        elif option == "B":
            self.show_difficulty_buttons()
        else:
            messagebox.showerror("Error", "Invalid option selected.")

    def show_difficulty_buttons(self):
        # Show difficulty selection buttons
        self.difficulty_label.place(x=150, y=250)
        self.easy_button.place(x=150, y=280)
        self.medium_button.place(x=250, y=280)
        self.hard_button.place(x=350, y=280)

    def hide_difficulty_buttons(self):
        # Hide difficulty selection buttons
        self.difficulty_label.place_forget()
        self.easy_button.place_forget()
        self.medium_button.place_forget()
        self.hard_button.place_forget()

    def start_option_a(self):
        option_a_window = tk.Toplevel(self.root)
        option_a_window.title("Option A: Enter your own Sudoku")
        self.setup_option_a(option_a_window)

    def setup_option_a(self, option_a_window):
        option_a_window.geometry("526x743")
        option_a_window.configure(bg="#91abc6")
        option_a_window.resizable(True, True)

        label = tk.Label(option_a_window, text="FILL IN THE NUMBERS AND CLICK SOLVE", font=('TkDefaultFont', 18), bg="#91abc6")
        label.place(x=0, y=50, width=526)

        label = tk.Label(option_a_window, text="", fg="#1e54a4", bg="#91abc6", font=('TkDefaultFont', 14))
        label.place(x=0, y=92, width=526)

        cells = {}

        def valid_number(P):
            out = (P.isdigit() or P == "") and len(P) < 2
            return out

        reg = option_a_window.register(valid_number)
 
        def draw_grid():
            frame = tk.Frame(option_a_window, bg="#91abc6")
            frame.place(x=42, y=151, width=443, height=443)
            font = ('TkTextFont', 14)

            for i in range(9):
                for j in range(9):
                    entry = tk.Entry(frame, bg="#fff", fg="#000", font=font, borderwidth=5, highlightbackground="#000",
                                     relief=tk.FLAT, justify="center", validate='key', validatecommand=(reg, '%P'))
                    entry.place(x=i * 49, y=j * 49, width=48, height=48)
                    cells[(i + 2, j + 1)] = entry

            for i in range(-1, 9, 3):
                tk.Frame(frame, bg="#000", width=441).place(x=0, y=(i + 1) * 49, height=2)

            for j in range(-1, 9, 3):
                tk.Frame(frame, bg="#000", width=2).place(x=(j + 1) * 49, y=0, height=441)

        def clear_values():
            label.configure(text="")
            for row in range(2, 11):
                for col in range(1, 10):
                    cell = cells[(row, col)]
                    cell.delete(0, "end")

        def get_values():
            board = []
            label.configure(text="")
            for row in range(2, 11):
                rows = []
                for col in range(1, 10):
                    val = cells[(row, col)].get()
                    if val == "":
                        rows.append(0)
                    else:
                        rows.append(int(val))
                board.append(rows)
            update_values(board)

        btn_solve = tk.Button(option_a_window, command=get_values, text="SOLVE", width=10, font=("TkTextFont", 14))
        btn_solve.grid(row=15, column=0, padx=10, pady=(10, 0))

        btn_clear = tk.Button(option_a_window, command=clear_values, text="CLEAR", width=10, font=("TkTextFont", 14))
        btn_clear.grid(row=15, column=1, padx=10, pady=(10, 0))

        btn_exit = tk.Button(option_a_window, command=option_a_window.destroy, text="EXIT", width=10, font=("TkTextFont", 14))
        btn_exit.grid(row=15, column=2, padx=10, pady=(10, 0))

        def update_values(s):
            sol = solve_sudoku(s, 0, 0)
            if sol:
                for rows in range(2, 11):
                    for col in range(1, 10):
                        cells[(rows, col)].delete(0, "end")
                        cells[(rows, col)].insert(0, s[rows - 2][col - 1])
                label.configure(text="SOLVED!")
            else:
                label.configure(text="NO SOLUTION!")

        draw_grid()

    def get_fixed_sudoku(self, difficulty):
        # Define fixed Sudoku puzzles for each difficulty level
        if difficulty == "easy":
            return [
                [5, 3, 0, 0, 7, 0, 0, 0, 0],
                [6, 0, 0, 1, 9, 5, 0, 0, 0],
                [0, 9, 8, 0, 0, 0, 0, 6, 0],
                [8, 0, 0, 0, 6, 0, 0, 0, 3],
                [4, 0, 0, 8, 0, 3, 0, 0, 1],
                [7, 0, 0, 0, 2, 0, 0, 0, 6],
                [0, 6, 0, 0, 0, 0, 2, 8, 0],
                [0, 0, 0, 4, 1, 9, 0, 0, 5],
                [0, 0, 0, 0, 8, 0, 0, 7, 9]
            ]
        elif difficulty == "medium":
            return [
                [0, 0, 0, 0, 0, 2, 0, 3, 0],
                [0, 8, 4, 0, 9, 0, 0, 0, 0],
                [0, 0, 0, 4, 0, 0, 0, 8, 0],
                [3, 4, 0, 0, 0, 6, 0, 0, 0],
                [0, 0, 7, 0, 0, 0, 2, 0, 0],
                [0, 0, 0, 2, 0, 0, 0, 9, 5],
                [0, 7, 0, 0, 0, 8, 0, 0, 0],
                [0, 0, 0, 0, 5, 0, 9, 6, 0],
                [0, 5, 0, 3, 0, 0, 0, 0, 0]
            ]
        elif difficulty == "hard":
            return [
                [8, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 3, 6, 0, 0, 0, 0, 0],
                [0, 7, 0, 0, 9, 0, 2, 0, 0],
                [0, 5, 0, 0, 0, 7, 0, 0, 0],
                [0, 0, 0, 0, 4, 5, 7, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 3, 0],
                [0, 0, 1, 0, 0, 0, 0, 6, 8],
                [0, 0, 8, 5, 0, 0, 0, 1, 0],
                [0, 9, 0, 0, 0, 0, 4, 0, 0]
            ]
        

    def start_option_b_easy(self):
        difficulty = "easy"
        sudoku_puzzle = self.get_fixed_sudoku(difficulty)
        self.display_sudoku(sudoku_puzzle, fixed=True, difficulty=difficulty)

    def start_option_b_medium(self):
        sudoku_puzzle = self.get_fixed_sudoku("medium")
        self.display_sudoku( sudoku_puzzle, fixed=True)

    def start_option_b_hard(self):
        sudoku_puzzle = self.get_fixed_sudoku("hard")
        self.display_sudoku( sudoku_puzzle, fixed=True)
    
    def display_unsolved_sudoku(self, sudoku):
        self.display_sudoku(sudoku)

    def start_option_b(self, difficulty, sudoku_puzzle):
        self.hide_difficulty_buttons()  # Hide difficulty selection buttons
        if difficulty == "easy":
            sudoku = self.get_fixed_sudoku("easy")
        elif difficulty == "medium":
            sudoku = self.get_fixed_sudoku("medium")
        elif difficulty == "hard":
            sudoku = self.get_fixed_sudoku("hard")
        else:
            return

    
    def solve_sudoku_difficulty(self, sudoku):
        solved_sudoku = self.solve_sudoku_wrapper(sudoku)
        if solved_sudoku:
            self.display_sudoku(solved_sudoku, fixed=True, difficulty=None)
        else:
            messagebox.showinfo("Sudoku Solver", "No solution exists for the given puzzle.")
    
    def solve_sudoku_wrapper(self, sudoku):
        # Make a deep copy of the original sudoku to avoid modifying it
        sudoku_copy = [row[:] for row in sudoku]
        if solve_sudoku(sudoku_copy, 0, 0):
            return sudoku_copy
        else:
            return None
        
    def display_sudoku(self, sudoku, fixed=False, difficulty=None):
        option_b_window = tk.Toplevel(self.root)
        option_b_window.title("Option B: Select an unsolved Sudoku")
        option_b_window.geometry("526x743")
        option_b_window.configure(bg="#91abc6")
        option_b_window.resizable(True, True)

        label_text = "YOUR SUDOKU" 
        label = tk.Label(option_b_window, text=label_text, font=("TkTextFont", 18), bg="#91abc6")
        label.place(x=0, y=50, width=526)

        #solve and exit buttons for option b
        btn_solve = tk.Button(option_b_window, command=lambda: self.solve_sudoku_difficulty(sudoku), text="SOLVE", width=10, font=("TkTextFont", 14))
        btn_solve.place(x=150, y=100)

        btn_exit = tk.Button(option_b_window, command=option_b_window.destroy, text="EXIT", width=10, font=("TkTextFont", 14))
        btn_exit.place(x=275, y=100)


        cells = {}

        def draw_grid():
            frame = tk.Frame(option_b_window, bg="#91abc6")
            frame.place(x=42, y=151, width=443, height=443)
            font = ('TkTextFont', 14)

            for i in range(9):
                for j in range(9):
                    entry = tk.Entry(frame, bg="#fff", fg="#000", font=font, borderwidth=5, highlightbackground="#000",
                           relief=tk.FLAT, justify="center")
                    entry.place(x=i * 49, y=j * 49, width=48, height=48)
                    cells[(i + 2, j + 1)] = entry
                    entry.insert(0, sudoku[i][j] if sudoku[i][j] != 0 else "")

            for i in range(-1, 9, 3):
                tk.Frame(frame, bg="#000", width=441).place(x=0, y=(i + 1) * 49, height=2)

            for j in range(-1, 9, 3):
                tk.Frame(frame, bg="#000", width=2).place(x=(j + 1) * 49, y=0, height=441)

        draw_grid()

        if fixed:
            label.config(text="YOUR SUDOKU: HIT SOLVE AND COMPARE")
       
N = 9
def is_safe(sudoku, row, col, num):
            for i in range(9):
                if sudoku[row][i] == num or sudoku[i][col] == num:
                    return False

            start_row = row - row % 3
            start_col = col - col % 3
            for i in range(3):
                for j in range(3):
                    if sudoku[start_row + i][start_col + j] == num:
                        return False
            return True

def solve_sudoku(sudoku, row, col):
            if row == N - 1 and col == N:
                return True

            if col == N:
                row += 1
                col = 0

            if sudoku[row][col] > 0:
                return solve_sudoku(sudoku, row, col + 1)

            for num in range(1, N + 1):
                if is_safe(sudoku, row, col, num):
                    sudoku[row][col] = num
                    if solve_sudoku(sudoku, row, col + 1):
                        return True
                sudoku[row][col] = 0
            return False


if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuSolverApp(root)
    root.mainloop()