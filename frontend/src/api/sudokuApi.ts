import axios from 'axios'

// const client = 'http://127.0.0.1:8000'
const client = 'https://sudoku-solver-egtr.onrender.com'

export const usePredict = async (file: File) => {
  try {
    const formData = new FormData()
    formData.append('file', file)
    
    const response = await axios(`${client}/predict`, {
      method: 'POST',
      headers: {
        'Content-Type': 'multipart/form-data'
      },
      data: formData
    });
    
    const data = response.data;
    if (!data) {
      console.error('Invalid API response:', data);
      throw new Error('Invalid API response');
    }

    return { 
      grid: data.grid,
      lowConfidenceCells: data.lowConfidenceCells || []
    }
  } catch (error) {
    console.error('Error in prediction:', error);
    throw error;
  }
};

export const useSolve = async (grid: Array<Array<number | null>>) => {
  try {
    const response = await axios(`${client}/solve`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      data: { grid }
    });
    
    const data = response.data;
    if (!data) {
      console.error('Invalid API response:', data);
      throw new Error('Invalid API response');
    }

    return { 
      solved_grid: data.grid
    }
  } catch (error) {
    console.error('Error in solving:', error);
    throw error;
  }
};