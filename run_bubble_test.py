# run_bubble_test.py
from algorithms.bubble import bubble_sort
from algorithms.base import Metrics

def run_demo():
    data = [5, 2, 9, 1, 5, 6]
    print("Input:", data)
    metrics = Metrics()
    gen = bubble_sort(data, metrics)
    step_no = 0
    for step in gen:
        step_no += 1
        arr = step.array
        highlights = step.highlights
        print(f"Step {step_no}: {arr}    highlights: {highlights}")
    print("Final sorted:", arr)
    print(f"Comparisons: {metrics.comparisons}, Swaps: {metrics.swaps}")

if __name__ == "__main__":
    run_demo()
