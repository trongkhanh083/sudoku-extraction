# 🧊 Sudoku Extraction

A computer vision application that extracts Sudoku puzzles from images and solves them using OCR and backtracking algorithms.

---

## 🚀 Features

- Extracts Sudoku grid from images using OpenCV
- Recognizes digits using Tesseract OCR
- Solves puzzles using backtracking algorithm
- Web interface via Streamlit

## ⚙️ Installation
   ```bash
   git clone https://github.com/trongkhanh083/sudoku-extraction.git
   cd sudoku-extraction
   pip install -r requirements.txt
   sudo apt install tesseract-ocr
   ```
   
## 🧠 Usage
  ```bash
  ./scripts/run_training.sh
  ```

### 🖼️ Web Interface
```bash
streamlit run streamlit_app.py
```
