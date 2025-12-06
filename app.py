# app.py
import tkinter as tk
from ui.canvas_view import CanvasView
from ui.controls import Controls
from core.animator import Animator
from algorithms.bubble import bubble_sort
from algorithms.selection import selection_sort
from algorithms.insertion import insertion_sort
from algorithms.merge import merge_sort
from algorithms.quick import quick_sort
from algorithms.base import Metrics
import random
import time

DEFAULT_SIZE = 40

ALG_MAP = {
    "Bubble Sort": bubble_sort,
    "Selection Sort": selection_sort,
    "Insertion Sort": insertion_sort,
    "Merge Sort": merge_sort,
    "Quick Sort": quick_sort
}

def make_legend(master):
    f = tk.Frame(master)
    items = [
        ("compare", "orange"),
        ("swap/write", "red"),
        ("pivot/key", "blue"),
        ("min/key", "purple"),
        ("sorted", "green"),
        ("default", "gray"),
    ]
    for label_text, color in items:
        box = tk.Canvas(f, width=18, height=12, highlightthickness=0)
        box.create_rectangle(0, 0, 18, 12, fill=color, outline="")
        box.pack(side="left", padx=(6,2))
        tk.Label(f, text=label_text, font=("Arial", 9)).pack(side="left", padx=(0,8))
    return f

def main():
    root = tk.Tk()
    root.title("Sorting Visualizer - Polished UI")
    root.geometry("1100x720")

    # Canvas
    canvas_view = CanvasView(root, bg="white", height=480)
    canvas_view.pack(fill="both", expand=False, padx=10, pady=10)

    # State
    data = [random.randint(5, 100) for _ in range(DEFAULT_SIZE)]
    canvas_view.draw_bars(data, {})

    metrics = Metrics()
    animator = Animator(canvas_view, root)
    animator.set_speed(60)

    # callbacks for Controls - we must provide on_step
    def on_generate(size):
        nonlocal data
        animator.stop()
        metrics.reset()
        data = [random.randint(5, 100) for _ in range(int(size))]
        canvas_view.draw_bars(data, {})
        controls.update_metrics_display(metrics)

    def on_start(alg_name):
        nonlocal data
        animator.stop()
        metrics.reset()
        alg_fn = ALG_MAP.get(alg_name)
        if alg_fn is None:
            return
        steps = alg_fn(data, metrics)
        start_time = time.perf_counter()
        controls.disable_while_running()
        run_state["start_time"] = start_time

        def metrics_update():
            if run_state["start_time"] is not None:
                metrics.set_time(time.perf_counter() - run_state["start_time"])
            controls.update_metrics_display(metrics)

        def on_finish():
            if run_state["start_time"] is not None:
                metrics.set_time(time.perf_counter() - run_state["start_time"])
            run_state["start_time"] = None
            controls.update_metrics_display(metrics)
            controls.enable_all()

        animator.start(steps, on_finish, metrics_update)

    def on_pause():
        animator.pause()
        # allow stepping while paused
        controls.enable_stepping_only()

    def on_resume():
        animator.resume()
        # resume continuous run: disable stepping
        controls.disable_while_running()

    def on_reset():
        nonlocal data
        animator.stop()
        metrics.reset()
        run_state["start_time"] = None
        canvas_view.draw_bars(data, {})
        controls.update_metrics_display(metrics)
        controls.enable_all()

    def on_speed_change(ms):
        animator.set_speed(ms)

    def on_size_change(sz):
        # only regenerate if user clicks Generate or we can auto-generate here
        pass

    def on_step():
        """
        Single-step behavior:
        If animator is running continuously, ignore (step button disabled).
        If paused and iterator present, advance exactly one step.
        If no iterator (fresh), create one and then step.
        """
        # if we don't have an iterator currently, create one in paused mode
        nonlocal data
        if animator._iter is None:
            # create iterator but do not start continuous animation
            # choose selected algorithm and create generator with metrics
            alg_name = controls.alg_var.get()
            alg_fn = ALG_MAP.get(alg_name)
            if alg_fn is None:
                return
            metrics.reset()
            animator.stop()
            iterator = alg_fn(data, metrics)
            # set animator internals: assign iterator and metrics callback but do not run
            animator._iter = iterator
            animator._metrics_cb = lambda: controls.update_metrics_display(metrics)
            # ensure stepping button enabled
            controls.enable_stepping_only()
        # now advance one step
        animator.step_once()
        # update metrics label after stepping
        controls.update_metrics_display(metrics)

    # Run-state container for timing
    run_state = {"start_time": None}

    # Create Controls and pass on_step
    controls = Controls(root,
                        alg_names=list(ALG_MAP.keys()),
                        on_generate=on_generate,
                        on_start=on_start,
                        on_pause=on_pause,
                        on_resume=on_resume,
                        on_reset=on_reset,
                        on_speed_change=on_speed_change,
                        on_size_change=on_size_change,
                        on_step=on_step)
    controls.frame.pack(fill="x", padx=10, pady=(0,6))

    # Legend
    legend = make_legend(root)
    legend.pack(fill="x", padx=10, pady=(0,8))

    # initial metrics
    controls.update_metrics_display(metrics)

    root.mainloop()

if __name__ == "__main__":
    main()
