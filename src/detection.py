import cv2
import numpy as np
import os

def preprocess_image(image_path):
    if isinstance(image_path, str):
        img = cv2.imread(image_path)
    else:
        img = image_path.copy()
    
    # convert to gray
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # apply gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    return img, blurred

def detect_edge(blurred_img):
    # apply Canny edge detection
    edged = cv2.Canny(blurred_img, 50, 150)
    
    # dilate the edge to close gap
    kernel = np.ones((3,3), np.uint8)
    edged = cv2.dilate(edged, kernel, iterations=1)

    return edged

def find_grid_contour(edged_img, raw_img):
    # find contour
    contour, _ = cv2.findContours(edged_img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # sort contour by area in descending order
    contour = sorted(contour, key=cv2.contourArea, reverse=True)
    
    # approximate the largest contour (should be the sudoku grid)
    grid_contour = None
    for c in contour:
        perimeter = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02*perimeter, True)
        
        # if the contour has 4 corners (likely the grid)
        if len(approx) == 4:
            grid_contour = approx
            break
            
    if grid_contour is not None:
        cv2.drawContours(raw_img, [grid_contour], -1, (0, 255, 0), 3)

    return grid_contour, raw_img

def perspective_transform(raw_img, grid_contour):
    # order the points in the contour: top-left, top-right, bottom-right, bottom-left
    point = grid_contour.reshape(4, 2)
    rect = np.zeros((4, 2), dtype='float32')
    
    # sum of coordinates
    s = np.sum(point, axis=1)
    rect[0] = point[np.argmin(s)] # top-left
    rect[2] = point[np.argmax(s)] # bottom-right
    
    # difference of coordinates
    diff = np.diff(point, axis=1)
    rect[1] = point[np.argmin(diff)] # top-right
    rect[3] = point[np.argmax(diff)] # bottom-left
    
    # define the dimensions of the output image
    width = height = 450
    
    # destination point for the transform
    dst = np.array([
        [0, 0],
        [width - 1, 0],
        [width - 1, height - 1],
        [0, height-1]
    ], dtype='float32')

    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(raw_img, M, (width, height))

    return warped

def main(raw_dir='data/raw'):
    os.makedirs('output/edged/', exist_ok=True)
    os.makedirs('output/warped/', exist_ok=True)

    for image in os.listdir(raw_dir):
        image_path = os.path.join(raw_dir, image)

        # get image name without extension
        image_name = os.path.splitext(image)[0]

        raw_img, blurred = preprocess_image(image_path)

        edged = detect_edge(blurred)
        edged_dir = os.path.join('output/edged/', f"{image_name}.png")
        cv2.imwrite(edged_dir, edged)
        print(f"Saved edged image to: {edged_dir}")

        grid_contour, raw_img = find_grid_contour(edged, raw_img)
        if grid_contour is None:
            print('Could not find Sudoku grid in {image}. Skipping...')
            continue
        else:
            warped = perspective_transform(raw_img, grid_contour)
            warped_dir = os.path.join('output/warped/', f"{image_name}.png")
            cv2.imwrite(warped_dir, warped)
            print(f"Saved warped image to: {warped_dir}")

if __name__=="__main__":
    main()