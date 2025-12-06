# algorithms/bubble.py
from typing import List, Iterator, Dict, Optional
from .base import Step, Metrics

def bubble_sort(arr: List[int], metrics: Optional[Metrics] = None) -> Iterator[Step]:
    """
    Bubble sort implemented as a generator.
    Yields Step objects at each comparison and swap so the UI can animate them.

    Signature:
        bubble_sort(arr, metrics=None) -> iterator of Step
    """
    a = arr[:]  # work on a copy so caller's list remains unchanged
    n = len(a)
    if metrics is None:
        # create a dummy metrics object to avoid checks
        metrics = Metrics()

    # Outer loop: shrink the unsorted portion
    for end in range(n, 1, -1):
        for i in range(1, end):
            # Comparison highlight
            metrics.comparisons += 1
            yield Step(a[:], {i-1: "orange", i: "orange"})
            if a[i-1] > a[i]:
                # perform swap
                a[i-1], a[i] = a[i], a[i-1]
                metrics.swaps += 1
                # Swap highlight
                yield Step(a[:], {i-1: "red", i: "red"})
    # Final: mark all as sorted (green)
    yield Step(a[:], {k: "green" for k in range(len(a))})
