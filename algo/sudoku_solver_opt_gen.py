import time

class SudokuSolver:
    def __init__(self, size=9):
        # The board stores the possible values for each cell (using bitmasking).
        self.size = size
        self.block_size = int(size ** 0.5)  # assuming size is a perfect square (e.g., 9 -> 3x3 block, 16 -> 4x4 block)
        self.board = [[(1 << size) - 1] * size for _ in range(size)]  # All values are possible initially (e.g., 0xFFFF for 16x16)

        # This array maps the final value from bitmask to actual digit.
        self.mask_to_value = [str(i + 1) for i in range(size)]

    def add(self, i, j, v):
        return self.set(i, j, 1 << (v - 1))  # v is 1-indexed

    def set(self, i, j, mask):
        prev = self.board[i][j]
        if prev == mask:
            return True
        if not (prev & mask):  # If the mask doesn't match the current state, return False.
            return False
        self.board[i][j] = mask
        return self.propagate(i, j, mask)

    def propagate(self, i, j, mask):
        for k in range(self.size):
            if k != j and not self.add_constraint(i, k, mask):
                return False
            if k != i and not self.add_constraint(k, j, mask):
                return False
            ii = (i // self.block_size) * self.block_size + (k // self.block_size)
            jj = (j // self.block_size) * self.block_size + (k % self.block_size)
            if (i != ii or j != jj) and not self.add_constraint(ii, jj, mask):
                return False
        return True

    def add_constraint(self, i, j, mask):
        new_mask = self.board[i][j] & ~mask
        if new_mask != self.board[i][j]:
            if new_mask == 0:
                return False  # If no valid possibilities are left, return False
            self.board[i][j] = new_mask
            if (new_mask - 1) & new_mask == 0:  # If only one possible value is left
                return self.propagate(i, j, new_mask)
        return True

    def find_ambiguous_cells(self):
        v = []
        for i in range(self.size):
            for j in range(self.size):
                mask = self.board[i][j]
                if mask & (mask - 1):  # if more than 1 value is possible
                    v.append((i, j))
        return v

    def solve(self):
        v = self.find_ambiguous_cells()
        return self.backtrack(0, v)

    def backtrack(self, k, v):
        if k == len(v):
            return True
        i, j = v[k]
        mask = self.board[i][j]
        if mask & (mask - 1):  # If there's more than one possibility
            snapshot = [row[:] for row in self.board]  # Save the current board state
            for cand in range(1, 1 << self.size, 1 << 1):  # Loop through possible values (1, 2, 4, 8, ...)
                if self.set(i, j, cand) and self.backtrack(k + 1, v):
                    return True
                self.board = snapshot  # Undo to the previous state
            return False
        else:
            return self.backtrack(k + 1, v)

    def get_solved_board(self):
        return [[self.mask_to_value[(self.board[i][j] % (self.size + 1)) - 1] for j in range(self.size)] for i in range(self.size)]


def solve_sudoku(board, size=9):
    solver = SudokuSolver(size=size)
    # Initialize the solver with the current board values
    for i in range(size):
        for j in range(size):
            if board[i][j] != 0:
                if not solver.add(i, j, board[i][j]):
                    return False

    # Propagate constraints and attempt to solve
    solver.solve()

    # Convert the solved board to its final values
    solved_board = solver.get_solved_board()

    # Copy the result back into the original board
    for i in range(size):
        for j in range(size):
            board[i][j] = int(solved_board[i][j])

    return True


# Example 16x16 Sudoku puzzle
puzzle_16x16 = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

# Call solver for 16x16 puzzle
start_time = time.time()
if solve_sudoku(puzzle_16x16, size=16):
    print("Solved 16x16 Sudoku puzzle:")
    for row in puzzle_16x16:
        print(row)
else:
    print("No solution found.")
end_time = time.time()

print(f"Time taken: {end_time - start_time:.2f} seconds.")
