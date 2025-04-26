import { useState } from 'react';
import { toast } from '@/hooks/use-toast';
import { usePredict, useSolve } from '@/api/sudokuApi';

export type SudokuGrid = Array<Array<number | null>>;

export const useSudokuSolver = () => {
  const [grid, setGrid] = useState<SudokuGrid>(
    Array(9).fill(null).map(() => Array(9).fill(null))
  );
  
  // Original grid as processed from the image (used to mark original cells)
  const [originalGrid, setOriginalGrid] = useState<SudokuGrid>(
    Array(9).fill(null).map(() => Array(9).fill(null))
  );
  
  // Loading states
  const [isProcessing, setIsProcessing] = useState(false);
  const [isSolving, setIsSolving] = useState(false);
  
  // Cells with low confidence from the ML model
  const [lowConfidenceCells, setLowConfidenceCells] = useState<Array<[number, number]>>([]);
  
  // Flag for whether the puzzle has been processed yet
  const [hasProcessedImage, setHasProcessedImage] = useState(false);
  
  // Function to process an uploaded image
  const processImage = async (file: File) => {
    try {
      setIsProcessing(true);
      
      // Call the predict function directly
      const response = await usePredict(file);
      
      const processedGrid = response.grid;
      const uncertainCells = response.lowConfidenceCells || [];
      
      setGrid(processedGrid);
      setOriginalGrid(processedGrid.map(row => [...row]));
      setLowConfidenceCells(uncertainCells);
      setHasProcessedImage(true);
      
      toast({
        title: "Success",
        description: "Sudoku puzzle processed successfully",
        variant: "default",
      });
    } catch (error) {
      console.error('Error processing image:', error);
      toast({
        title: "Error",
        description: "Failed to process the image. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsProcessing(false);
    }
  };
  
  // Function to solve the current grid
  const solvePuzzle = async () => {
    try {
      setIsSolving(true);
      
      // Call the solve function directly with the grid
      const response = await useSolve(grid);
      
      if (response.solved_grid) {
        setGrid(response.solved_grid);
        toast({
          title: "Success",
          description: "Puzzle solved successfully!",
          variant: "default",
        });
      } else {
        toast({
          title: "Error",
          description: "This puzzle has no valid solution",
          variant: "destructive",
        });
      }
    } catch (error) {
      console.error('Error solving puzzle:', error);
      toast({
        title: "Error",
        description: "Failed to solve the puzzle. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsSolving(false);
    }
  };
  
  // Function to reset the grid to the original state
  const resetGrid = () => {
    setGrid(originalGrid.map(row => [...row]));
    toast({
      title: "Info",
      description: "Grid reset to original state",
      variant: "default",
    });
  };
  
  // Function to clear the grid entirely
  const clearGrid = () => {
    setGrid(Array(9).fill(null).map(() => Array(9).fill(null)));
    setOriginalGrid(Array(9).fill(null).map(() => Array(9).fill(null)));
    setLowConfidenceCells([]);
    setHasProcessedImage(false);
    toast({
      title: "Info",
      description: "Grid cleared",
      variant: "default",
    });
  };
  
  return {
    grid,
    originalGrid,
    lowConfidenceCells,
    isProcessing,
    isSolving,
    hasProcessedImage,
    processImage,
    solvePuzzle,
    resetGrid,
    clearGrid,
    updateGrid: setGrid
  };
};