# algorithms/quick.py
from typing import List, Iterator, Optional
from .base import Step, Metrics

def quick_sort(arr: List[int], metrics: Optional[Metrics] = None) -> Iterator[Step]:
    """
    Quick sort (Lomuto partition) implemented as a generator.
    Yields Steps for comparisons and swaps; recursively partitions using yield from.
    """
    a = arr[:]  # operate on local copy
    if metrics is None:
        metrics = Metrics()
    n = len(a)

    def partition(low: int, high: int) -> int:
        pivot = a[high]
        i = low - 1
        for j in range(low, high):
            metrics.comparisons += 1
            # show compare (j) with pivot (high)
            yield Step(a[:], {j: "orange", high: "blue"})
            if a[j] < pivot:
                i += 1
                a[i], a[j] = a[j], a[i]
                metrics.swaps += 1
                yield Step(a[:], {i: "red", j: "red"})
        # place pivot in correct position
        a[i+1], a[high] = a[high], a[i+1]
        metrics.swaps += 1
        yield Step(a[:], {i+1: "red", high: "red"})
        return i+1

    # recursive quicksort using generator-friendly approach
    def sort(low: int, high: int):
        if low < high:
            # run partition as a generator to yield internal steps
            # partition produces yields and then returns pivot index via value, but Python generator return isn't easy to capture here.
            # We'll implement partition inline for simplicity and yields (same logic as above but inline).
            pivot = a[high]
            i = low - 1
            for j in range(low, high):
                metrics.comparisons += 1
                yield Step(a[:], {j: "orange", high: "blue"})
                if a[j] < pivot:
                    i += 1
                    a[i], a[j] = a[j], a[i]
                    metrics.swaps += 1
                    yield Step(a[:], {i: "red", j: "red"})
            a[i+1], a[high] = a[high], a[i+1]
            metrics.swaps += 1
            yield Step(a[:], {i+1: "red", high: "red"})
            p = i + 1
            # sort left and right partitions
            yield from sort(low, p-1)
            yield from sort(p+1, high)

    yield from sort(0, n-1)
    yield Step(a[:], {idx: "green" for idx in range(n)})
