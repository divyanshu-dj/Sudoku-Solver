#include <stdio.h>
#include <stdbool.h>
#include <time.h>

#define SIZE 9

bool isValid(int board[SIZE][SIZE], int row, int col, int ch) {
    // Check the row
    for (int i = 0; i < SIZE; i++) {
        if (board[row][i] == ch) return false;
    }

    // Check the column
    for (int i = 0; i < SIZE; i++) {
        if (board[i][col] == ch) return false;
    }

    // Check the 3x3 sub-grid
    int startRow = (row / 3) * 3;
    int startCol = (col / 3) * 3;
    for (int i = startRow; i < startRow + 3; i++) {
        for (int j = startCol; j < startCol + 3; j++) {
            if (board[i][j] == ch) return false;
        }
    }

    return true;
}

bool solve(int board[SIZE][SIZE]) {
    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            if (board[i][j] == 0) { // Find an empty cell
                for (int ch = 1; ch <= 9; ch++) { // Try numbers 1 to 9
                    if (isValid(board, i, j, ch)) {
                        board[i][j] = ch; // Assign the number
                        if (solve(board)) { // Recursively solve the rest
                            return true;
                        }
                        board[i][j] = 0; // Undo the assignment if not valid
                    }
                }
                return false; // If no valid number found, return false
            }
        }
    }
    return true; // Puzzle solved
}

void printBoard(int board[SIZE][SIZE]) {
    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            printf("%d ", board[i][j]);
        }
        printf("\n");
    }
}

int main() {
    // Array of puzzles
    int puzzles[9][SIZE][SIZE] = {
        {
            {5, 3, 0, 0, 7, 0, 0, 0, 0},
            {6, 0, 0, 1, 9, 5, 0, 0, 0},
            {0, 9, 8, 0, 0, 0, 0, 6, 0},
            {8, 0, 0, 0, 6, 0, 0, 0, 3},
            {4, 0, 0, 8, 0, 3, 0, 0, 1},
            {7, 0, 0, 0, 2, 0, 0, 0, 6},
            {0, 6, 0, 0, 0, 0, 2, 8, 0},
            {0, 0, 0, 4, 1, 9, 0, 0, 5},
            {0, 0, 0, 0, 8, 0, 0, 7, 9}
        },
        {
            {0, 2, 0, 6, 0, 8, 0, 0, 0},
            {5, 8, 0, 0, 0, 9, 7, 0, 0},
            {0, 0, 0, 0, 4, 0, 0, 0, 0},
            {3, 7, 0, 0, 0, 0, 5, 0, 0},
            {6, 0, 0, 0, 0, 0, 0, 0, 4},
            {0, 0, 8, 0, 0, 0, 0, 1, 3},
            {0, 0, 0, 0, 2, 0, 0, 0, 0},
            {0, 0, 9, 8, 0, 0, 0, 3, 6},
            {0, 0, 0, 3, 0, 6, 0, 9, 0}
        },
        {
            {0, 0, 0, 0, 0, 0, 0, 1, 2},
            {0, 0, 0, 0, 3, 5, 0, 0, 0},
            {0, 0, 0, 4, 0, 0, 0, 0, 0},
            {0, 0, 8, 0, 0, 0, 0, 0, 0},
            {0, 0, 0, 5, 0, 1, 0, 0, 0},
            {0, 0, 0, 0, 0, 0, 6, 0, 0},
            {0, 0, 0, 0, 0, 4, 0, 0, 0},
            {0, 0, 0, 9, 8, 0, 0, 0, 0},
            {9, 5, 0, 0, 0, 0, 0, 0, 0}
        },
        {
            {0, 0, 0, 6, 0, 0, 0, 0, 0},
            {0, 0, 0, 0, 0, 0, 4, 0, 0},
            {0, 0, 0, 0, 0, 0, 0, 0, 3},
            {0, 0, 7, 0, 0, 9, 0, 2, 0},
            {0, 0, 0, 0, 4, 0, 0, 0, 0},
            {0, 5, 0, 7, 0, 0, 8, 0, 0},
            {1, 0, 0, 0, 0, 0, 0, 0, 0},
            {0, 0, 3, 0, 0, 0, 0, 0, 0},
            {0, 0, 0, 0, 0, 0, 2, 0, 0}
        },
        {
            {0, 0, 0, 8, 0, 0, 0, 0, 0},
            {0, 0, 0, 0, 0, 0, 0, 6, 0},
            {0, 0, 0, 0, 0, 0, 0, 0, 4},
            {0, 3, 0, 0, 5, 0, 0, 0, 0},
            {0, 0, 0, 7, 0, 8, 0, 0, 0},
            {0, 0, 0, 0, 6, 0, 0, 2, 0},
            {5, 0, 0, 0, 0, 0, 0, 0, 0},
            {0, 2, 0, 0, 0, 0, 0, 0, 0},
            {0, 0, 0, 0, 0, 4, 0, 0, 0}
        },
        {
            {0, 0, 0, 0, 0, 0, 2, 0, 0},
            {0, 0, 0, 0, 3, 0, 0, 0, 9},
            {0, 0, 0, 7, 0, 0, 0, 0, 0},
            {0, 0, 0, 0, 0, 9, 0, 0, 0},
            {0, 0, 4, 0, 0, 0, 3, 0, 0},
            {0, 9, 0, 0, 0, 0, 0, 0, 0},
            {0, 0, 0, 0, 0, 0, 0, 8, 0},
            {0, 5, 0, 0, 0, 0, 0, 0, 0},
            {0, 0, 2, 0, 0, 0, 0, 0, 0}
        },
        {
            {0, 0, 0, 0, 0, 0, 0, 1, 0},
            {0, 0, 0, 0, 6, 0, 0, 0, 0},
            {0, 0, 0, 0, 0, 8, 0, 0, 0},
            {0, 4, 0, 0, 0, 0, 0, 0, 3},
            {0, 0, 0, 0, 7, 0, 0, 0, 0},
            {9, 0, 0, 0, 0, 0, 0, 6, 0},
            {0, 0, 0, 5, 0, 0, 0, 0, 0},
            {0, 0, 1, 0, 0, 0, 0, 0, 0},
            {0, 8, 0, 0, 0, 0, 0, 0, 0}
        },
        {
            {0, 0, 0, 0, 0, 0, 0, 0, 1},
            {0, 0, 0, 0, 0, 2, 0, 0, 0},
            {0, 0, 0, 3, 0, 0, 0, 0, 0},
            {0, 0, 7, 0, 0, 0, 0, 0, 0},
            {0, 6, 0, 0, 0, 0, 0, 0, 0},
            {0, 0, 0, 0, 0, 5, 0, 0, 0},
            {0, 0, 0, 0, 0, 0, 0, 0, 0},
            {1, 0, 0, 0, 0, 0, 0, 0, 0},
            {0, 0, 0, 0, 4, 0, 0, 0, 0}
        }
    };

    for (int puzzleIndex = 0; puzzleIndex < 9; puzzleIndex++) {
        int board[SIZE][SIZE];
        for (int i = 0; i < SIZE; i++) {
            for (int j = 0; j < SIZE; j++) {
                board[i][j] = puzzles[puzzleIndex][i][j];
            }
        }

        // Start timing
        clock_t start = clock();

        // Solve the puzzle
        bool solved = solve(board);

        // End timing
        clock_t end = clock();
        double duration = ((double) (end - start)) / CLOCKS_PER_SEC;

        // Output the result and time taken
        printf("Puzzle %d %s\n", puzzleIndex + 1, solved ? "solved!" : "not solvable");
        printf("Time taken: %.6f seconds\n", duration);

        // Uncomment this to print the solved board
        // if (solved) {
        //     printBoard(board);
        // }
        printf("-----------------------------\n");
    }

    return 0;
}
