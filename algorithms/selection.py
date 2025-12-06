# algorithms/selection.py
from typing import List, Iterator, Dict, Optional
from .base import Step, Metrics

def selection_sort(arr: List[int], metrics: Optional[Metrics] = None) -> Iterator[Step]:
    a = arr[:]
    if metrics is None:
        metrics = Metrics()
    n = len(a)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            metrics.comparisons += 1
            yield Step(a[:], {min_idx: "purple", j: "orange"})
            if a[j] < a[min_idx]:
                min_idx = j
                yield Step(a[:], {min_idx: "purple"})
        if min_idx != i:
            a[i], a[min_idx] = a[min_idx], a[i]
            metrics.swaps += 1
            yield Step(a[:], {i: "red", min_idx: "red"})
    yield Step(a[:], {k: "green" for k in range(n)})
