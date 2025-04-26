from flask import Flask, request, jsonify
import cv2
import numpy as np
import tensorflow as tf
import ctypes
from flask_cors import CORS
from sudoku_solver_optimized import solve_sudoku

app = Flask(__name__)

CORS(app)

# Load the trained model
model = tf.keras.models.load_model("./model/full_model.h5")
solver = ctypes.CDLL('./algo/lib_sudoku_solver.so')
solver.solve.argtypes = [ctypes.POINTER(ctypes.c_int * 9 * 9)]
solver.solve.restype = ctypes.c_bool


def preprocess(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(img_gray, (9, 9), 0)
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                   cv2.THRESH_BINARY, 11, 2)
    inverted = cv2.bitwise_not(thresh)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    morph = cv2.morphologyEx(inverted, cv2.MORPH_OPEN, kernel)
    result = cv2.dilate(morph, kernel, iterations=1)
    return result

def main_outline(contours):
    biggest = np.array([])
    max_area = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 50:
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            if area > max_area and len(approx) == 4:
                biggest = approx
                max_area = area
    return biggest, max_area

def reframe(points):
    points = points.reshape((4, 2))
    points_new = np.zeros((4, 1, 2), dtype=np.int32)
    add = points.sum(1)
    points_new[0] = points[np.argmin(add)]
    points_new[3] = points[np.argmax(add)]
    diff = np.diff(points, axis=1)
    points_new[1] = points[np.argmin(diff)]
    points_new[2] = points[np.argmax(diff)]
    return points_new

def splitcells(img):
    rows = np.vsplit(img, 9)
    boxes = []
    for row in rows:
        cols = np.hsplit(row, 9)
        boxes.extend(cols)
    return boxes

def CropCell(cells):
    cropped = []
    for cell in cells:
        h, w = cell.shape
        cell = cell[5:h-5, 5:w-5]
        cropped.append(cell)
    return cropped

def preprocess_image(img):
    img = cv2.resize(img, (28, 28))
    if np.mean(img) > 127:
        img = 255 - img
    img = img.astype('float32') / 255.0
    img = np.expand_dims(img, axis=-1)
    img = np.expand_dims(img, axis=0)
    return img

def read_cells(cells, model):
    result = []
    for cell in cells:
        processed = preprocess_image(cell)
        predictions = model.predict(processed, verbose=0)
        classIndex = np.argmax(predictions, axis=1)
        probabilityValue = np.amax(predictions)
        result.append(classIndex[0] if probabilityValue > 0.5 else 0)
    return result

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    npimg = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    # img = cv2.imread('../images/5.jpg')
    if img is None:
        return jsonify({'error': 'Invalid image'}), 400

    threshold = preprocess(img)
    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    biggest, maxArea = main_outline(contours)

    if biggest.size == 0:
        return jsonify({'error': 'No Sudoku grid found'}), 400

    biggest = reframe(biggest)
    pts1 = np.float32(biggest)
    pts2 = np.float32([[0, 0], [450, 0], [0, 450], [450, 450]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imagewrap = cv2.warpPerspective(img, matrix, (450, 450))
    imagewrap_gray = cv2.cvtColor(imagewrap, cv2.COLOR_BGR2GRAY)

    cells = splitcells(imagewrap_gray)
    cropped_cells = CropCell(cells)
    grid = read_cells(cropped_cells, model)
    grid = np.array(grid).reshape(9, 9)
    print(grid)
    return jsonify({'grid': grid.tolist()})


def solve_with_c(grid):
    print(grid)
    c_grid = (ctypes.c_int * 9 * 9)()
    for i in range(9):
        for j in range(9):
            c_grid[i][j] = grid[i][j]
    print(c_grid)
    success = solver.solve(ctypes.byref(c_grid))
    print(success)
    solved = [[c_grid[i][j] for j in range(9)] for i in range(9)]
    return solved if success else None


@app.route('/solve', methods=['POST'])
def solve_route():
    data = request.get_json()
    grid = data.get('grid')
    if not grid or any(len(row) != 9 for row in grid):
        return jsonify({'error': 'Invalid grid format'}), 400

    if solve_sudoku(grid):
        return jsonify({'solved': True, 'grid': grid})
    else:
        return jsonify({'solved': False}), 200

@app.route('/')
def home():
    return "Hello World!"

if __name__ == '__main__':
    app.run(debug=True)
