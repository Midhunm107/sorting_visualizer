# algorithms/insertion.py
from typing import List, Iterator, Dict, Optional
from .base import Step, Metrics

def insertion_sort(arr: List[int], metrics: Optional[Metrics] = None) -> Iterator[Step]:
    a = arr[:]
    if metrics is None:
        metrics = Metrics()
    n = len(a)
    for i in range(1, n):
        key = a[i]
        j = i - 1
        # show key being considered
        yield Step(a[:], {i: "blue"})
        while j >= 0:
            metrics.comparisons += 1
            yield Step(a[:], {j: "orange", j+1: "orange"})
            if a[j] > key:
                a[j+1] = a[j]
                metrics.swaps += 1
                yield Step(a[:], {j: "red", j+1: "red"})
                j -= 1
            else:
                break
        a[j+1] = key
        yield Step(a[:], {j+1: "purple"})
    yield Step(a[:], {k: "green" for k in range(n)})
