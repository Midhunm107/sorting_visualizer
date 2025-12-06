# tests/test_algorithms.py

import pytest
from algorithms.base import Metrics
from algorithms.bubble import bubble_sort
from algorithms.selection import selection_sort
from algorithms.insertion import insertion_sort
from algorithms.merge import merge_sort
from algorithms.quick import quick_sort

# A list of algorithm functions to test
ALGORITHMS = [
    bubble_sort,
    selection_sort,
    insertion_sort,
    merge_sort,
    quick_sort,
]

# Different sample arrays to verify correctness
TEST_CASES = [
    [],
    [1],
    [5, 2],
    [3, 1, 2],
    [5, 3, 1, 4, 2],
    [10, 3, 5, 7, 2, 9, 1],
    [4, 4, 4, 4],                 # duplicates
    [9, 1, 8, 2, 7, 3, 6, 4, 5],  # reverse-like pattern
]


@pytest.mark.parametrize("alg", ALGORITHMS)
@pytest.mark.parametrize("arr", TEST_CASES)
def test_algorithms_produce_sorted(alg, arr):
    """
    Ensures every algorithm returns a completely sorted array at the end.
    """
    metrics = Metrics()
    steps = alg(arr, metrics)

    final_step = None
    for step in steps:
        final_step = step

    # If no steps produced (empty list case)
    final_array = final_step.array if final_step else arr

    assert final_array == sorted(arr), f"{alg.__name__} failed on input {arr}"
