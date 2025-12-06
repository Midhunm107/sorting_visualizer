# algorithms/base.py
from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class Step:
    array: List[int]
    highlights: Dict[int, str]  # index -> color tag (e.g., {0: "orange", 1: "red"})

class Metrics:
    """Lightweight metrics object you can pass into algorithms (optional)."""
    def __init__(self):
        self.comparisons = 0
        self.swaps = 0
        self.time = 0.0

    def reset(self):
        self.comparisons = 0
        self.swaps = 0
        self.time = 0.0

    def set_time(self, t: float):
        self.time = float(t)
