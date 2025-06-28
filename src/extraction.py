import pytesseract
from PIL import Image
import cv2
import numpy as np
import os

def extract_cell(warped_img):
    gray = cv2.cvtColor(warped_img, cv2.COLOR_BGR2GRAY)

    # threshold to get binary image
    _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)

    # divide the image to 9x9 grid
    cell = []
    row = np.vsplit(thresh, 9)

    for r in row:
        col = np.hsplit(r, 9)
        for c in col:
            cell.append(c)

    return cell

def recognize_digit(cell_img):
    _, thresh = cv2.threshold(cell_img, 128, 255, cv2.THRESH_BINARY_INV)

    # convert to pil image for tesseract
    pil_img = Image.fromarray(thresh)

    # configure tesseract for digit
    custom_config = r'--oem 3 --psm 10 outputbase digits'
    digit = pytesseract.image_to_string(pil_img, config=custom_config).strip()
    
    return digit if digit else '0'

def extract_sudoku_matrix(cell):
    sudoku = np.zeros((9, 9), dtype=int)
    
    # extract 9x9 sudoku grid
    for i in range(9):
        for j in range(9):
            c = cell[i*9 + j]
            digit = recognize_digit(c)
            digit = digit[-1:] if digit > '10' else digit
            sudoku[i, j] = int(digit) if digit.isdigit() else 0
    
    return sudoku

def main(warped_dir='output/warped'):
    os.makedirs('output/sudoku_grid', exist_ok=True)

    for image in os.listdir(warped_dir):
        image_path = os.path.join(warped_dir, image)

        # get image name without extension
        image_name = os.path.splitext(image)[0]

        warped = cv2.imread(image_path)

        cell = extract_cell(warped)

        sudoku = extract_sudoku_matrix(cell)

        grid_dir = os.path.join('output/sudoku_grid', f"{image_name}.txt")
        with open(grid_dir, 'w') as f:
            for row in sudoku:
                row_str = ' '.join(map(str, row))
                f.write(row_str + '\n')
        
        print(f"Save Sudoku grid to: {grid_dir}")


if __name__=="__main__":
    main()