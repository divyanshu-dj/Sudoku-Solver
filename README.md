# 🧩 Sudoku Solver AI Web App

A full-stack web application that predicts Sudoku puzzles from images and solves them instantly!  
Built with **React**, **Flask**, **TensorFlow**, and sudoku solver algo written in C, C++, Python.

---

## 🚀 Tech Stack
- **Frontend**: React + TypeScript + Tanstack + Axios + Tailwind + Vite
- **Backend**: Flask
- **Machine Learning**: TensorFlow (CNN for digit recognition), OpenCV, Python, Numpy
- **Sudoku Solver**: C (fastest)(under 10ms), C++, Python(slowest)(under 200ms)

---

## ✨ Features
- Upload a photo of a Sudoku puzzle.
- Automatic detection and isolation of the Sudoku grid using OpenCV.
- ML model (CNN) predicts each digit from the uploaded image.
- Users can correct any mistakes made by the model predictions.
- Solve the puzzle instantly using optimized solving algorithms.
- Integrated a fast C-based backtracking solver for enhanced performance.
- Built an end-to-end pipeline from image upload to solution generation.
- Combined machine learning predictions with traditional solving techniques to maximize accuracy.
- Fast, responsive, and user-friendly interface built with React.


---

## 📂 Project Structure
```
/algo
    ├── sudoku_solver.c, .cpp, .go, .py
    └── lib_sudoku_solver.so

/backend
    ├── app.py
    ├── sudoku_solver_optimized.py
    └── model/full_model.h5

/frontend
    ├── src/
    ├── public/
    └── package.json

/images
    └── sample Sudoku images

sudoku_solver.py
.gitignore
README.md
```

---

## ⚙️ How It Works
1. User uploads an image of a Sudoku puzzle.
2. Backend processes the image using OpenCV to detect the Sudoku grid.
3. Each cell is fed into a CNN model to recognize digits.
4. User verifies/corrects the detected digits.
5. The corrected grid is sent back to the backend.
6. Backend solves the Sudoku using a fast C library.
7. Solution is displayed to the user.

---

## 📦 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/sudoku-solver.git
cd sudoku-solver
```

---

### 2. Backend Setup (Flask)
- Navigate to the backend:
```bash
cd backend
```

- Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

- Compile the C Sudoku Solver:
```bash
gcc -shared -o ../algo/lib_sudoku_solver.so -fPIC ../algo/sudoku_solver.c
```

- Ensure the trained TensorFlow model exists at:
```
backend/model/full_model.h5
```

- Start the Flask server:
```bash
python app.py
```

---

### 3. Frontend Setup (React)
- Navigate to the frontend:
```bash
cd frontend
```

- Install frontend dependencies:
```bash
npm install
```

- Create a `.env` file:
```bash
VITE_BACKEND_URL=http://localhost:5000
```

- Start the React development server:
```bash
npm run dev
```

---

## 🛠 API Endpoints

| Endpoint | Method | Description |
|:---------|:-------|:------------|
| `/predict` | POST | Upload an image, returns predicted Sudoku grid |
| `/solve`   | POST | Submit corrected Sudoku grid, returns solved grid |
| `/`        | GET  | Health check (returns "Hello World!") |

---

## 📸 Screenshots
> _Coming soon!_  
> (You can add UI screenshots or a GIF demo here for better visibility!)

---

## 🧠 Future Improvements
- Better digit recognition with enhanced data augmentation.
- Add animated solving visualization.
- Deploy live version (Frontend on Vercel, Backend on Render).
- Add dark/light mode toggle on frontend.

---

## 🙏 Acknowledgements
- [TensorFlow](https://www.tensorflow.org/) for machine learning.
- [OpenCV](https://opencv.org/) for image processing.
- [Flask](https://flask.palletsprojects.com/) for the backend server.
- [React](https://react.dev/) for building the frontend.

---

## 📜 License
This project is licensed under the MIT License - feel free to use and modify it.

---

# ✨ Thank You for Checking Out Sudoku Solver AI Web App! ✨
