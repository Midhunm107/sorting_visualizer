# algorithms/merge.py
from typing import List, Iterator, Optional
from .base import Step, Metrics

def merge_sort(arr: List[int], metrics: Optional[Metrics] = None) -> Iterator[Step]:
    """
    In-place merge sort visualizer (works on a local copy).
    Yields Steps during merging showing comparisons and writes.
    """
    a = arr[:]  # work on a copy
    if metrics is None:
        metrics = Metrics()

    n = len(a)

    def sort(l: int, r: int):
        # sort segment [l, r) (r is exclusive)
        if r - l <= 1:
            return
        m = (l + r) // 2
        # sort left and right halves
        yield from sort(l, m)
        yield from sort(m, r)

        # merge left [l,m) and right [m,r)
        left = a[l:m]
        right = a[m:r]
        i = j = 0
        k = l
        while i < len(left) and j < len(right):
            # highlight compare positions
            metrics.comparisons += 1
            yield Step(a[:], {l + i: "orange", m + j: "orange"})
            if left[i] <= right[j]:
                a[k] = left[i]
                i += 1
            else:
                a[k] = right[j]
                j += 1
            # count this write as a "move" (approx. swaps)
            metrics.swaps += 1
            # highlight the position written
            yield Step(a[:], {k: "red"})
            k += 1

        # copy remaining elements of left
        while i < len(left):
            a[k] = left[i]
            i += 1
            metrics.swaps += 1
            yield Step(a[:], {k: "red"})
            k += 1

        # copy remaining elements of right
        while j < len(right):
            a[k] = right[j]
            j += 1
            metrics.swaps += 1
            yield Step(a[:], {k: "red"})
            k += 1

    # kick off recursive sort
    yield from sort(0, n)
    # final highlight
    yield Step(a[:], {idx: "green" for idx in range(n)})
