
import React from 'react';

const Header = () => {
  return (
    <header className="py-8 sm:py-12 animate-fade-in">
      <div className="space-y-2 text-center max-w-2xl mx-auto">
        <h1 className="font-semibold text-4xl md:text-5xl tracking-tight">Sudoku Solver</h1>
        <p className="text-muted-foreground text-lg md:text-xl max-w-md mx-auto">
          Upload a picture of your Sudoku puzzle and we'll solve it for you.
        </p>
      </div>
    </header>
  );
};

export default Header;
