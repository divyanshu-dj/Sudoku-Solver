// SudokuGrid.tsx
import React, { useEffect, useState } from 'react';
import SudokuCell from './SudokuCell';

type SudokuGrid = Array<Array<number | null>>;

interface SudokuGridProps {
  grid: SudokuGrid;
  originalGrid: SudokuGrid;
  isLoading?: boolean;
  lowConfidenceCells?: Array<[number, number]>;
  onGridChange: (newGrid: SudokuGrid) => void;
}

const SudokuGrid: React.FC<SudokuGridProps> = ({
  grid,
  originalGrid,
  isLoading = false,
  lowConfidenceCells = [],
  onGridChange,
}) => {
  const [displayGrid, setDisplayGrid] = useState<SudokuGrid>(grid);

  // Update the display grid when the input grid changes
  useEffect(() => {
    setDisplayGrid(grid);
  }, [grid]);

  const handleCellChange = (rowIndex: number, colIndex: number, value: number | null) => {
    const newGrid = [...displayGrid.map(row => [...row])];
    newGrid[rowIndex][colIndex] = value;
    setDisplayGrid(newGrid);
    onGridChange(newGrid);
  };

  // Check if a cell is part of the original grid
  const isOriginalCell = (rowIndex: number, colIndex: number) => {
    return originalGrid[rowIndex][colIndex] !== null;
  };

  // Check if a cell is marked as low confidence
  const isLowConfidence = (rowIndex: number, colIndex: number) => {
    return lowConfidenceCells.some(([r, c]) => r === rowIndex && c === colIndex);
  };

  return (
    <div className="sudoku-grid-container mx-auto max-w-md animate-scale-in">
      <div className="sudoku-grid aspect-square">
        {displayGrid.map((row, rowIndex) =>
          row.map((cellValue, colIndex) => (
            <SudokuCell
              key={`${rowIndex}-${colIndex}`}
              value={cellValue}
              isOriginal={isOriginalCell(rowIndex, colIndex)}
              rowIndex={rowIndex}
              colIndex={colIndex}
              isLoading={isLoading}
              isLowConfidence={isLowConfidence(rowIndex, colIndex)}
              onChange={handleCellChange}
            />
          ))
        )}
      </div>
    </div>
  );
};

export default SudokuGrid;
