import React, { useState, useRef, useEffect } from 'react';
import { cn } from '@/lib/utils';

interface SudokuCellProps {
  value: number | null;
  isOriginal: boolean;
  rowIndex: number;
  colIndex: number;
  isLoading?: boolean;
  isLowConfidence?: boolean;
  onChange: (rowIndex: number, colIndex: number, value: number | null) => void;
}

const SudokuCell: React.FC<SudokuCellProps> = ({
  value,
  isOriginal,
  rowIndex,
  colIndex,
  isLoading = false,
  isLowConfidence = false,
  onChange,
}) => {
  const inputRef = useRef<HTMLInputElement>(null);
  const [isFocused, setIsFocused] = useState(false);
  const [localValue, setLocalValue] = useState<string>(value ? value.toString() : '');

  // Update local value when prop changes
  useEffect(() => {
    setLocalValue(value ? value.toString() : '');
  }, [value]);

  // Check if cell should be highlighted as part of a box
  const isInHighlightedBox = 
    Math.floor(rowIndex / 3) % 2 === 1 && Math.floor(colIndex / 3) % 2 === 0 ||
    Math.floor(rowIndex / 3) % 2 === 0 && Math.floor(colIndex / 3) % 2 === 1;

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    // Allow navigation with arrow keys
    if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'].includes(e.key)) {
      e.preventDefault();
      navigateWithArrows(e.key);
    }
    
    // Clear cell on Delete or Backspace
    if (e.key === 'Delete' || e.key === 'Backspace') {
      e.preventDefault();
      setLocalValue('');
      onChange(rowIndex, colIndex, null);
    }
    
    // Handle numeric input directly on keydown
    if (/^[1-9]$/.test(e.key)) {
      e.preventDefault();
      setLocalValue(e.key);
      onChange(rowIndex, colIndex, parseInt(e.key, 10));
      
      // Auto advance to next cell on valid input
      if (colIndex < 8) {
        setTimeout(() => navigateWithArrows('ArrowRight'), 10);
      } else if (rowIndex < 8) {
        // Move to first cell of next row
        setTimeout(() => {
          const nextCell = document.querySelector(
            `[data-row="${rowIndex + 1}"][data-col="0"] input`
          ) as HTMLElement;
          if (nextCell) nextCell.focus();
        }, 10);
      }
    }
    
    // Prevent non-numeric input except for control keys
    if (
      !/^[1-9]$/.test(e.key) && 
      !['Backspace', 'Delete', 'Tab', 'Enter', 'ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'].includes(e.key)
    ) {
      e.preventDefault();
    }
  };

  const navigateWithArrows = (key: string) => {
    let nextRow = rowIndex;
    let nextCol = colIndex;

    switch (key) {
      case 'ArrowUp':
        nextRow = (rowIndex - 1 + 9) % 9;
        break;
      case 'ArrowDown':
        nextRow = (rowIndex + 1) % 9;
        break;
      case 'ArrowLeft':
        nextCol = (colIndex - 1 + 9) % 9;
        break;
      case 'ArrowRight':
        nextCol = (colIndex + 1) % 9;
        break;
    }

    // Find the next cell element and focus it
    const nextCell = document.querySelector(
      `[data-row="${nextRow}"][data-col="${nextCol}"] input`
    ) as HTMLElement;
    
    if (nextCell) {
      nextCell.focus();
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = e.target.value;
    
    if (newValue === '') {
      setLocalValue('');
      onChange(rowIndex, colIndex, null);
      return;
    }
    
    // Take only the last character entered
    const lastChar = newValue.slice(-1);
    
    if (/^[1-9]$/.test(lastChar)) {
      const numValue = parseInt(lastChar, 10);
      setLocalValue(lastChar);
      onChange(rowIndex, colIndex, numValue);
    }
  };

  // Handle direct clicks and touch input
  const handleClick = () => {
    if (!isOriginal && !isLoading && inputRef.current) {
      inputRef.current.focus();
    }
  };

  return (
    <div
      data-row={rowIndex}
      data-col={colIndex}
      className={cn(
        'sudoku-cell relative',
        isInHighlightedBox && 'bg-sudoku-cell/70',
        isFocused && 'bg-sudoku-cell-active',
        isLowConfidence && 'bg-sudoku-cell-highlight',
        isLoading && 'animate-pulse-subtle',
        !isOriginal && !isLoading && 'cursor-text'
      )}
      onClick={handleClick}
    >
      <input
        ref={inputRef}
        type="text"
        inputMode="numeric"
        pattern="[1-9]"
        maxLength={1}
        value={localValue}
        onChange={handleChange}
        onKeyDown={handleKeyDown}
        onFocus={() => setIsFocused(true)}
        onBlur={() => setIsFocused(false)}
        className={cn(
          'sudoku-cell-input text-center w-full h-full absolute inset-0',
          isOriginal ? 'sudoku-original font-bold' : 'text-blue-600',
          isLoading && 'opacity-50'
        )}
        readOnly={isOriginal || isLoading}
        disabled={isLoading}
        aria-label={`Row ${rowIndex + 1}, Column ${colIndex + 1}`}
      />
    </div>
  );
};

export default SudokuCell;
