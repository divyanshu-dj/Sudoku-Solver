import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({ apiKey: import.meta.env.GOOGLE_GENAI_API_KEY });

export async function convertSudokuImageToArray(imageFile: File): Promise<number[][]> {
  try {
    const base64Image = await fileToBase64(imageFile);
    const prompt = "Analyze this Sudoku image and return only a 2D array representation. Empty cells should be 0.";
    const contents = [
        {
          inlineData: {
            mimeType: "image/jpeg",
            data: base64Image,
          },
        },
        { text: prompt },
    ];
    const response = await ai.models.generateContent({
        model: "gemini-2.0-flash",
        contents: contents,
    });
    return parseResponseToSudokuArray(response.text);
  } catch (error) {
    console.error('Error calling Gemini API:', error);
    throw error;
  }
}

function fileToBase64(file: File): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => {
      const base64String = reader.result as string;
      resolve(base64String.split(',')[1]);
    };
    reader.onerror = error => reject(error);
  });
}

function parseResponseToSudokuArray(text: string): number[][] {
  try {
    const arrayText = text.replace(/``````/g, '').trim();
    return JSON.parse(arrayText);
  } catch (error) {
    console.error('Error parsing Gemini response:', error);
    throw new Error('Failed to parse Sudoku array from Gemini response');
  }
}
