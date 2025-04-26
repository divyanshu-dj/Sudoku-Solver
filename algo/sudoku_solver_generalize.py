import time
import math

# Backtracking Sudoku Solver for any size grid
def is_valid_move(board, row, col, num, n, subgrid_size):
    # Check if the number is not in the current row, column, and subgrid
    for i in range(n):
        if board[row][i] == num or board[i][col] == num:
            return False
        
    # Check subgrid (sqrt(n) x sqrt(n) block)
    start_row = (row // subgrid_size) * subgrid_size
    start_col = (col // subgrid_size) * subgrid_size
    
    for i in range(subgrid_size):
        for j in range(subgrid_size):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def solve_sudoku(board, n, subgrid_size):
    for row in range(n):
        for col in range(n):
            if board[row][col] == 0:  # Find an empty spot (0)
                for num in range(1, n + 1):
                    if is_valid_move(board, row, col, num, n, subgrid_size):
                        board[row][col] = num
                        if solve_sudoku(board, n, subgrid_size):
                            return True
                        board[row][col] = 0  # Backtrack
                return False
    return True

# Function to print the board nicely
def print_board(board):
    for row in board:
        print(" ".join(str(x) if x != 0 else '.' for x in row))

# Example Sudoku puzzles with different sizes (4x4, 9x9, 16x16 for demonstration)

puzzles = [
    # 4x4 Sudoku (simple example)
    [  # Easy
        [1, 0, 0, 0],
        [0, 0, 3, 0],
        [0, 2, 0, 0],
        [0, 0, 0, 4]
    ],
    [  # Hard
        [0, 0, 0, 0],
        [0, 3, 0, 0],
        [4, 0, 0, 3],
        [0, 0, 0, 0]
    ],
    # 9x9 Sudoku (standard example)
    [  # Easy 9x9
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ],
    # 16x16 Sudoku (for larger grids)
    # [  # Easy 16x16 (partial example)
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # ],
    # Easy 16x16 Sudoku Puzzle with some clues filled
    [
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 12, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 14, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15]
    ],


]

# Solve and time each puzzle
for level, puzzle in enumerate(puzzles, start=1):
    n = len(puzzle)  # The size of the board (n x n)
    subgrid_size = int(math.sqrt(n))  # Subgrid size (e.g., 2 for 4x4 Sudoku, 3 for 9x9, etc.)
    
    print(f"\nLevel {level} Puzzle ({n}x{n}):")
    print_board(puzzle)

    start_time = time.time()
    if solve_sudoku(puzzle, n, subgrid_size):
        end_time = time.time()
        print(f"\nLevel {level} Solved Puzzle:")
        print_board(puzzle)
        print(f"Execution Time: {end_time - start_time:.4f} seconds")
    else:
        print("No solution exists")
