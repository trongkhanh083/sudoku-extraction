import streamlit as st
from PIL import Image
import numpy as np
import cv2
from src.detection import preprocess_image, detect_edge, find_grid_contour, perspective_transform
from src.extraction import extract_cell, extract_sudoku_matrix

# Page configuration
st.set_page_config(
    page_title="Sudoku Extraction",
    page_icon="🧊",
    layout="wide"
)

def display_sudoku_grid(grid):
    html = """
    <style>
    .sudoku-grid {
        border: 3px solid #333;
        border-collapse: collapse;
        margin: 20px auto;
    }
    .sudoku-grid td {
        border: 1px solid #999;
        width: 50px;
        height: 50px;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
    }
    .sudoku-grid tr:nth-child(3n) td {
        border-bottom: 3px solid #333;
    }
    .sudoku-grid td:nth-child(3n) {
        border-right: 3px solid #333;
    }
    </style>
    <table class="sudoku-grid">
    """
    
    for i in range(9):
        html += "<tr>"
        for j in range(9):
            value = grid[i][j] if grid[i][j] != 0 else ""
            html += f"<td>{value}</td>"
        html += "</tr>"
    html += "</table>"
    
    st.markdown(html, unsafe_allow_html=True)

st.title("Sudoku Extraction from Image")
st.markdown("Upload an image of a Sudoku puzzle and extract the grid")

uploaded = st.file_uploader("Choose an image...", type=["jpg","jpeg","png"])
if uploaded is not None:
    file_bytes = np.asarray(bytearray(uploaded.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.subheader("Raw Image")
        st.image(image, channels="BGR")

    if 'edged' not in st.session_state:
        st.session_state.edged = None
    if 'warped' not in st.session_state:
        st.session_state.warped = None
    if 'grid' not in st.session_state:
        st.session_state.grid = None

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.subheader("Detection")
        if st.button("Run Detection"):
            with st.spinner("Detecting image ..."):
                raw_img, blurred = preprocess_image(image)

                edged = detect_edge(blurred)
                st.session_state.edged = edged

                grid_contour, raw_img = find_grid_contour(edged, raw_img)  
                if grid_contour is None:
                    st.error("Could not find Sudoku grid in the image")
                else:
                    warped = perspective_transform(raw_img, grid_contour)
                    st.session_state.warped = warped

        if st.session_state.edged is not None:
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Edged Image")
                st.image(st.session_state.edged, clamp=True)
            with col2:
                st.subheader("Warped Image")
                st.image(st.session_state.warped, channels="BGR")
            st.success("Detecting completed!")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.subheader("Extraction")
        if st.button("Run Extraction") and st.session_state.warped is not None:
            with st.spinner("Extracting digit..."):
                cell = extract_cell(st.session_state.warped)
                sudoku_grid = extract_sudoku_matrix(cell)
                st.session_state.grid = sudoku_grid

        if st.session_state.grid is not None:
            st.subheader("Sudoku Grid")
            display_sudoku_grid(st.session_state.grid)
            st.success("Extracting completed!")