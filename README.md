# Sorting Algorithm Visualizer

A desktop GUI app (Tkinter) that visualizes sorting algorithms step-by-step.

## Features
- Visualizes: Bubble, Selection, Insertion, Merge, Quick sorts.
- Color-coded highlights:
  - orange = comparison
  - red = swap / write
  - blue = pivot / key
  - purple = min/key
  - green = sorted
- Controls: Algorithm dropdown, Size slider, Speed slider, Generate, Start, Pause, Resume, Step, Reset.
- Live metrics: comparisons, swaps, elapsed time.
- Single-step mode for teaching/demos.

## Requirements
- Python 3.8+ (Tkinter included).
- Create and activate a virtual environment (recommended).

## Setup & Run

source venv/bin/activate

# windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

pip install -r requirements.txt
python app.py
