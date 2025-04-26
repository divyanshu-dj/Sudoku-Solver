import time

class SudokuSolver:
    def __init__(self):
        # The board stores the possible values for each cell (using bitmasking).
        self.board = [[0x1FF] * 9 for _ in range(9)]  # 0x1FF = 111111111 in binary (all 9 values possible)

        # Map a single-bit mask to its corresponding digit (1–9). If mask_to_value is misaligned, adjust accordingly.
        self.mask_to_value = {
            1 << i: str(i + 1) for i in range(9)
        }

    def add(self, i, j, v):
        return self.set(i, j, 1 << (v - 1))  # v is 1-indexed

    def set(self, i, j, mask):
        prev = self.board[i][j]
        if prev == mask:
            return True
        if not (prev & mask):  # mask conflict
            return False
        self.board[i][j] = mask
        return self.propagate(i, j, mask)

    def propagate(self, i, j, mask):
        for k in range(9):
            if k != j and not self._remove_mask(i, k, mask):
                return False
            if k != i and not self._remove_mask(k, j, mask):
                return False
            ii = (i // 3) * 3 + (k // 3)
            jj = (j // 3) * 3 + (k % 3)
            if (i, j) != (ii, jj) and not self._remove_mask(ii, jj, mask):
                return False
        return True

    def _remove_mask(self, i, j, mask):
        new_mask = self.board[i][j] & ~mask
        if new_mask != self.board[i][j]:
            if new_mask == 0:
                return False
            self.board[i][j] = new_mask
            # if only one bit remains, propagate further
            if new_mask & (new_mask - 1) == 0:
                return self.propagate(i, j, new_mask)
        return True

    def solve(self):
        ambiguous = [(i, j) for i in range(9) for j in range(9) if self.board[i][j] & (self.board[i][j] - 1)]
        return self._backtrack(ambiguous, 0)

    def _backtrack(self, ambiguous, idx):
        if idx == len(ambiguous):
            return True
        i, j = ambiguous[idx]
        mask = self.board[i][j]
        if mask & (mask - 1):  # multiple possibilities
            snapshot = [row[:] for row in self.board]
            bit = 1
            while bit <= 0x1FF:
                if mask & bit:
                    if self.set(i, j, bit) and self._backtrack(ambiguous, idx + 1):
                        return True
                    self.board = [row[:] for row in snapshot]
                bit <<= 1
            return False
        return self._backtrack(ambiguous, idx + 1)

    def get_solved(self):
        # Convert the bitmask board to integers
        solved = [[0] * 9 for _ in range(9)]
        for i in range(9):
            for j in range(9):
                mask = self.board[i][j]
                if mask in self.mask_to_value:
                    solved[i][j] = int(self.mask_to_value[mask])
                else:
                    # Shouldn't happen if solved correctly
                    solved[i][j] = 0
        return solved


def solve_sudoku(board):
    """
    Solves a 9x9 Sudoku in-place using constraint propagation and backtracking.
    :param board: List[List[int]] with 0 for empty cells and 1-9 for given digits.
    :return: True if solved successfully, False otherwise.
    """
    solver = SudokuSolver()
    # Initialize constraints
    print(board)
    for i in range(9):
        for j in range(9):
            val = board[i][j]
            if val:
                if not solver.add(i, j, val):
                    return False
    # Solve
    if not solver.solve():
        return False
    solved = solver.get_solved()
    # Write back to input board
    for i in range(9):
        for j in range(9):
            board[i][j] = solved[i][j]
    return True

# Example usage:
if __name__ == "__main__":
    puzzle = [
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
    start = time.time()
    if solve_sudoku(puzzle):
        print("Solved:")
        for row in puzzle:
            print(row)
    else:
        print("No solution exists")
    print(f"Time: {time.time() - start:.4f}s")
