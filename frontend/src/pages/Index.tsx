
import { useState } from 'react';
import Header from '@/components/Header';
import ImageUploader from '@/components/ImageUploader';
import SudokuGrid from '@/components/SudokuGrid';
import { useSudokuSolver } from '@/hooks/useSudokuSolver';
import { Button } from '@/components/ui/button';
import { RotateCw, Play, RefreshCw, X } from 'lucide-react';

const Index = () => {
  const [uploadedImage, setUploadedImage] = useState<File | null>(null);
  
  const {
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
    updateGrid
  } = useSudokuSolver();

  const handleImageUpload = (file: File) => {
    setUploadedImage(file);
  };

  const handleProcessImage = () => {
    if (uploadedImage) {
      processImage(uploadedImage);
    }
  };

  return (
    <div className="min-h-screen bg-background text-foreground">
      <div className="container px-4 py-8 max-w-4xl mx-auto">
        <Header />
        
        <main className="space-y-8">
          <ImageUploader onImageUpload={handleImageUpload} />
          
          {uploadedImage && !hasProcessedImage && (
            <div className="flex justify-center animate-fade-in">
              <Button
                className="button-primary"
                onClick={handleProcessImage}
                disabled={isProcessing}
              >
                {isProcessing ? (
                  <>
                    <RotateCw className="mr-2 h-4 w-4 animate-spin" />
                    Processing...
                  </>
                ) : (
                  <>Process Image</>
                )}
              </Button>
            </div>
          )}
          
          {hasProcessedImage && (
            <div className="space-y-6 animate-fade-in">
              <SudokuGrid
                grid={grid}
                originalGrid={originalGrid}
                isLoading={isSolving}
                lowConfidenceCells={lowConfidenceCells}
                onGridChange={updateGrid}
              />
              
              <div className="flex flex-wrap gap-3 justify-center">
                <Button
                  variant="default"
                  className="flex items-center gap-2"
                  onClick={solvePuzzle}
                  disabled={isSolving}
                >
                  {isSolving ? (
                    <>
                      <RotateCw className="h-4 w-4 animate-spin" />
                      Solving...
                    </>
                  ) : (
                    <>
                      <Play className="h-4 w-4" />
                      Solve Puzzle
                    </>
                  )}
                </Button>
                
                <Button
                  variant="secondary"
                  className="flex items-center gap-2"
                  onClick={resetGrid}
                  disabled={isSolving}
                >
                  <RefreshCw className="h-4 w-4" />
                  Reset
                </Button>
                
                <Button
                  variant="outline"
                  className="flex items-center gap-2"
                  onClick={clearGrid}
                  disabled={isSolving}
                >
                  <X className="h-4 w-4" />
                  Clear
                </Button>
              </div>
              
              {lowConfidenceCells.length > 0 && (
                <div className="text-sm text-muted-foreground text-center">
                  <p>
                    Highlighted cells have low confidence. Please verify and correct if needed.
                  </p>
                </div>
              )}
            </div>
          )}
        </main>
        
        <footer className="mt-16 text-center text-sm text-muted-foreground">
          <p>
            Use the keyboard to navigate the grid. Arrow keys to move between cells.
          </p>
        </footer>
      </div>
    </div>
  );
};

export default Index;
