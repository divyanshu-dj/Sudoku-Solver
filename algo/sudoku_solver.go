package main

import (
	"fmt"
	"sync"
	"time"
)

const SIZE = 9

// Utility functions to print the Sudoku board
func printBoard(board [][]int) {
	for i := 0; i < SIZE; i++ {
		for j := 0; j < SIZE; j++ {
			fmt.Printf("%d ", board[i][j])
		}
		fmt.Println()
	}
}

// Checks whether placing 'num' at position (row, col) is valid
func isValid(board [][]int, row, col, num int) bool {
	// Check the row
	for i := 0; i < SIZE; i++ {
		if board[row][i] == num {
			return false
		}
	}

	// Check the column
	for i := 0; i < SIZE; i++ {
		if board[i][col] == num {
			return false
		}
	}

	// Check the 3x3 subgrid
	startRow := row - row%3
	startCol := col - col%3
	for i := 0; i < 3; i++ {
		for j := 0; j < 3; j++ {
			if board[startRow+i][startCol+j] == num {
				return false
			}
		}
	}
	return true
}

// Solves the Sudoku using backtracking and goroutines for parallelization
func solve(board [][]int, wg *sync.WaitGroup) bool {
	defer wg.Done() // Decrement the counter when the function finishes

	// Find the next empty cell
	for row := 0; row < SIZE; row++ {
		for col := 0; col < SIZE; col++ {
			if board[row][col] == 0 {
				// Try every number from 1 to 9
				for num := 1; num <= SIZE; num++ {
					if isValid(board, row, col, num) {
						board[row][col] = num

						// Create a new WaitGroup for the next level of recursion
						var innerWg sync.WaitGroup
						innerWg.Add(1)
						go func() {
							if solve(board, &innerWg) {
								wg.Done() // Notify the outer WaitGroup
								return
							}
							board[row][col] = 0
							innerWg.Done() // Mark this recursive branch as done
						}()
						return false
					}
				}
				return false // No valid number found, need to backtrack
			}
		}
	}
	return true // Puzzle solved
}

func main() {
	// Define a Sudoku puzzle (you can modify it for testing)
	board := [][]int{
		{5, 3, 0, 0, 7, 0, 0, 0, 0},
		{6, 0, 0, 1, 9, 5, 0, 0, 0},
		{0, 9, 8, 0, 0, 0, 0, 6, 0},
		{8, 0, 0, 0, 6, 0, 0, 0, 3},
		{4, 0, 0, 8, 0, 3, 0, 0, 1},
		{7, 0, 0, 0, 2, 0, 0, 0, 6},
		{0, 6, 0, 0, 0, 0, 2, 8, 0},
		{0, 0, 0, 4, 1, 9, 0, 0, 5},
		{0, 0, 0, 0, 8, 0, 0, 7, 9},
	}

	var wg sync.WaitGroup
	wg.Add(1)

	// Start timing
	start := time.Now()

	// Solve the Sudoku puzzle
	if solve(board, &wg) {
		fmt.Println("Puzzle solved:")
		printBoard(board)
	} else {
		fmt.Println("Puzzle could not be solved")
	}

	// Wait for all goroutines to finish
	wg.Wait()

	// End timing
	duration := time.Since(start)
	fmt.Println("Time taken:", duration.Seconds(), "seconds")
}
