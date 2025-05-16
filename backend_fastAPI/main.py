from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import numpy as np
import cv2
from model.model import predict_pipeline
# from llm.llm_predict import llm_predict
from solver_algo.sudoku_solver_optimized import solve_sudoku

app = FastAPI()

class SudokuGrid(BaseModel):
    grid: List[List[int]]

origins = [
    "https://sudoku-solver-beta-navy.vercel.app",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()
    npimg = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    if img is None:
        return {"error": "Invalid image"}

    ml_grid = predict_pipeline(img)
    # llm_grid = llm_predict(npimg)
    print(ml_grid)
    # print(llm_grid)
    return {"grid": ml_grid.tolist()}

@app.post("/solve")
async def solve(data: SudokuGrid):
    grid = data.grid
    if not grid or any(len(row) != 9 for row in grid):
        return {"error": "Invalid grid format"}

    if solve_sudoku(grid):
        return {"solved": True, "grid": grid}
    else:
        return {"solved": False}

