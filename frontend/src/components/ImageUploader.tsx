
import React, { useState, useCallback, useRef } from 'react';
import { Upload, Image as ImageIcon } from 'lucide-react';

interface ImageUploaderProps {
  onImageUpload: (file: File) => void;
}

const ImageUploader = ({ onImageUpload }: ImageUploaderProps) => {
  const [isDragging, setIsDragging] = useState(false);
  const [preview, setPreview] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDragOver = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      handleFile(file);
    }
  }, []);

  const handleFileChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      handleFile(file);
    }
  }, []);

  const handleFile = (file: File) => {
    // Check if file is an image
    if (!file.type.match('image.*')) {
      return;
    }

    // Create a preview
    const reader = new FileReader();
    reader.onload = (e) => {
      if (e.target?.result) {
        setPreview(e.target.result as string);
        onImageUpload(file);
      }
    };
    reader.readAsDataURL(file);
  };

  const handleClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <div className="mb-8 animate-fade-in animation-delay-100">
      <input 
        type="file" 
        ref={fileInputRef}
        onChange={handleFileChange} 
        accept="image/*"
        className="hidden" 
      />
      
      {!preview ? (
        <div 
          className={`drop-area ${isDragging ? 'active' : ''}`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={handleClick}
        >
          <Upload className="h-10 w-10 text-muted-foreground" />
          <div className="space-y-1 text-center">
            <p className="font-medium">Drag and drop your Sudoku image</p>
            <p className="text-sm text-muted-foreground">Or click to browse</p>
          </div>
        </div>
      ) : (
        <div className="animate-scale-in">
          <div className="relative mx-auto max-w-md rounded-lg overflow-hidden shadow-md">
            <img 
              src={preview} 
              alt="Sudoku preview" 
              className="w-full h-auto" 
            />
            <button 
              className="absolute top-2 right-2 bg-background/80 backdrop-blur-sm text-foreground p-2 rounded-full shadow-sm hover:bg-background transition-colors"
              onClick={() => setPreview(null)}
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M18 6 6 18"></path>
                <path d="m6 6 12 12"></path>
              </svg>
            </button>
          </div>
          <div className="flex justify-center mt-4">
            <button
              className="button-secondary flex items-center gap-2"
              onClick={handleClick}
            >
              <ImageIcon className="h-4 w-4" />
              Change Image
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ImageUploader;
