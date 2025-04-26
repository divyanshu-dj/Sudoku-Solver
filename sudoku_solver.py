import time
import copy
from image_processor import SudokuImageProcessor

# Backtracking Sudoku Solver
def is_valid_move(board, row, col, num):
    # Check if the number is not in the current row, column, and 3x3 subgrid
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
        if board[row//3*3 + i//3][col//3*3 + i%3] == num:
            return False
    return True

def solve_sudoku(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid_move(board, row, col, num):
                        board[row][col] = num
                        if solve_sudoku(board):
                            return True
                        board[row][col] = 0
                return False
    return True


def solve_and_time(board):
        """
        Solve the Sudoku puzzle and measure execution time
        """
        # Create a deep copy of the board to preserve original input
        board_copy = copy.deepcopy(board)
        
        print("\nInput Puzzle:")
        for row in board_copy:
            print(row)
        
        start_time = time.time()
        
        # Attempt to solve
        if solve_sudoku(board_copy):
            end_time = time.time()
            
            print("\nSolved Puzzle:")
            for row in board_copy:
                print(row)
            
            print(f"Execution Time: {end_time - start_time:.4f} seconds")
            
            return board_copy
        else:
            print("No solution exists for this Sudoku puzzle.")
            return None

def main():
    # Initialize the image processor and solver
    processor = SudokuImageProcessor()
    
    # Choose image source
    print("Select Sudoku Image Source:")
    print("1. Upload Image")
    print("2. Capture from Camera")
    
    choice = input("Enter your choice (1/2): ")
    
    # Get Sudoku board from image
    if choice == '1':
        board = processor.upload_image()
    elif choice == '2':
        board = processor.capture_image()
    else:
        print("Invalid choice!")
        return
    
    # Solve the puzzle if board is successfully extracted
    if board:
        # Validate board (ensure it's a 9x9 grid)
        if len(board) != 9 or any(len(row) != 9 for row in board):
            print("Invalid Sudoku board. Must be a 9x9 grid.")
            return
        
        # Solve the puzzle
        solved_board = solve_and_time(board)
        
        # Optional: Validate solution
        if solved_board:
            print("\nSolution Verification:")
            print("Sudoku puzzle solved successfully!")
    else:
        print("Failed to extract Sudoku board from image.")

if __name__ == "__main__":
    main()



# Solve and time each puzzle
# for level, puzzle in enumerate(puzzles, start=1):
    # print(f"\nInput Puzzle:")
    # for row in puzzle:
    #     print(row)

    # start_time = time.time()
    # if solve_sudoku(board):
    #     end_time = time.time()
    #     print(f"\nSolved Puzzle")
    #     for row in board:
    #         print(row)
    #     print(f"Execution Time: {end_time - start_time:.4f} seconds")
    # else:
    #     print("No solution exists")
