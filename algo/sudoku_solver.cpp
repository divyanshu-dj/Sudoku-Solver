#include <bits/stdc++.h>
using namespace std;

#define fast_io() ios_base::sync_with_stdio(false); cin.tie(NULL);

bool isValid(vector<vector<int>>& board, int row, int col, int ch) {
    for (int i = 0; i < 9; i++) {
        if (board[i][col] == ch) return false;
        if (board[row][i] == ch) return false;
        if (board[3*(row/3)+i/3][3*(col/3)+i%3] == ch) return false;
    }
    return true;
}

bool solve(vector<vector<int>>& board) {
    for (int i = 0; i < board.size(); i++) {
        for (int j = 0; j < board[0].size(); j++) {
            if (board[i][j] == 0) {
                for (int ch = 1; ch <= 9; ch++) {
                    if (isValid(board, i, j, ch)) {
                        board[i][j] = ch;
                        if (solve(board) == true) {
                            return true;
                        }
                        board[i][j] = 0;
                    }
                }
                return false;
            }
        }
    }
    return true;
}

int main() {
    fast_io();

    // Start timing
    // auto start = chrono::high_resolution_clock::now();

    vector<vector<vector<int>>> puzzles = {
    {  // Easy
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
    {  // Medium
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
    {  // Hard
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
    {  // Expert
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
    {  // Fiendish
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
    {  // Diabolical
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
    {  // Extreme
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
    {  // Master
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


    for (size_t puzzleIndex = 0; puzzleIndex < puzzles.size(); puzzleIndex++) {
        vector<vector<int>> board = puzzles[puzzleIndex];

        // Start timing
        auto start = chrono::high_resolution_clock::now();

        // Solve the puzzle
        bool solved = solve(board);

        // End timing
        auto end = chrono::high_resolution_clock::now();
        chrono::duration<double> duration = end - start;

        // Output the result and time taken
        cout << "Puzzle " << puzzleIndex + 1 << (solved ? " solved!" : " not solvable") << endl;
        cout << "Time taken: " << duration.count() << " seconds" << endl;

        // Print the solved board
        // if (solved) {
        //     for (int i = 0; i < 9; i++) {
        //         for (int j = 0; j < 9; j++) {
        //             cout << board[i][j] << " ";
        //         }
        //         cout << endl;
        //     }
        // }
        cout << "-----------------------------\n";
    }

    return 0;
}
