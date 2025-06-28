#!/usr/bin/env bash
# scripts/run_training.sh
set -e
export PYTHONPATH="$(pwd)"

# Load defaults from configs/default.yaml
RAW_DIR=$(grep '^raw_dir:' configs/default.yaml    | awk '{print $2}')
EDGED_DIR=$(grep '^edged_dir:' configs/default.yaml    | awk '{print $2}')
WARPED_DIR=$(grep '^warped_dir:' configs/default.yaml    | awk '{print $2}')
SUDOKU_GRID_DIR=$(grep '^sudoku_grid_dir:' configs/default.yaml    | awk '{print $2}')

# 1) Edge detection, perspective transformation
python -m src.detection \
  --raw_dir  "$RAW_DIR" \
  --edged_dir  "$EDGED_DIR" \
  --warped_dir  "$WARPED_DIR" \


# 2) Extraction Sudoku 9x9 grid
python -m src.extraction \
  --warped_dir  "$WARPED_DIR" \
  --sudoku_grid_dir  "$SUDOKU_GRID_DIR" \

echo
echo "All done! You finished the Sudoku Extraction project. Enjoy your result!"