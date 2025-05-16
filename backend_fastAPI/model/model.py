
from pathlib import Path
import cv2
import numpy as np
import tensorflow as tf

BASE_DIR = Path(__file__).resolve(strict=True).parent

model = tf.keras.models.load_model(f"{BASE_DIR}/trained_pipeline_model.h5")
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])


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

# def preprocess_image(img):
#     img = cv2.resize(img, (28, 28))
#     if np.mean(img) > 127:
#         img = 255 - img
#     img = img.astype('float32') / 255.0
#     img = np.expand_dims(img, axis=-1)
#     img = np.expand_dims(img, axis=0)
#     return img

# PARALLEL/BATCH PREDICTION
def preprocess_image(img):
    img = cv2.resize(img, (28, 28))
    if np.mean(img) > 127:
        img = 255 - img
    img = img.astype('float32') / 255.0
    img = np.expand_dims(img, axis=-1)
    return img


# def read_cells(cells, model):
#     result = []
#     for i, cell in enumerate(cells):
#         processed = preprocess_image(cell)
#         predictions = model.predict(processed, verbose=0)
#         classIndex = np.argmax(predictions, axis=1)
#         probabilityValue = np.amax(predictions)
#         # print(f"Cell {i+1}/81 prediction: {classIndex[0]} (prob {probabilityValue:.2f})")  # debug
#         result.append(classIndex[0] if probabilityValue > 0.5 else 0)
#     return result

# PARALLEL/BATCH PREDICTION
def read_cells(cells, model):
    preprocessed_cells = []
    
    for cell in cells:
        processed = preprocess_image(cell)  # shape: (1, 28, 28, 1)
        preprocessed_cells.append(processed)  # remove the batch dim to collect all together
    
    preprocessed_cells = np.stack(preprocessed_cells, axis=0)  # shape: (81, 28, 28, 1)
    
    predictions = model.predict(preprocessed_cells, verbose=0)  # batch predict
    class_indices = np.argmax(predictions, axis=1)
    probabilities = np.amax(predictions, axis=1)

    result = [cls if prob > 0.5 else 0 for cls, prob in zip(class_indices, probabilities)]
    return result



"""
Predicts the Sudoku grid from the given image using the trained pipeline model.
:param image: Input image of the Sudoku puzzle.
:return: Predicted Sudoku grid.
"""
def predict_pipeline(img):
    # img = cv2.imread('../../images/5.jpg')
    if img is None:
        return 'Invalid image'

    threshold = preprocess(img)
    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    biggest, maxArea = main_outline(contours)

    if biggest.size == 0:
        return 'No Sudoku grid found'

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
    return grid