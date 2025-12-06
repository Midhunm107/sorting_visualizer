# core/animator.py
from typing import Iterator, Callable, Optional
from algorithms.base import Step

class Animator:
    def __init__(self, canvas_view, root):
        self.canvas_view = canvas_view
        self.root = root
        self._iter: Optional[Iterator] = None
        self._running = False
        self.speed = 60
        self._after_id = None
        self._finish_cb: Optional[Callable] = None
        self._metrics_cb: Optional[Callable] = None

    def set_speed(self, ms: int):
        self.speed = max(1, int(ms))

    def start(self, steps_iter: Iterator, on_finish: Callable = None, metrics_update_cb: Callable = None):
        """
        Start running the iterator continuously (schedules frames with .after).
        """
        self.stop()
        self._iter = steps_iter
        self._finish_cb = on_finish
        self._metrics_cb = metrics_update_cb
        self._running = True
        self._step()

    def _step(self):
        if not self._running or self._iter is None:
            return
        try:
            step: Step = next(self._iter)
            self.canvas_view.draw_bars(step.array, step.highlights)
            if self._metrics_cb:
                self._metrics_cb()
            self._after_id = self.root.after(self.speed, self._step)
        except StopIteration:
            self._running = False
            self._iter = None
            if self._finish_cb:
                self._finish_cb()

    def pause(self):
        if not self._running:
            return
        self._running = False
        if self._after_id:
            self.root.after_cancel(self._after_id)
            self._after_id = None

    def resume(self):
        if self._iter and not self._running:
            self._running = True
            self._step()

    def stop(self):
        """
        Stop everything and forget the iterator.
        """
        self.pause()
        self._iter = None
        self._after_id = None
        self._finish_cb = None
        self._metrics_cb = None

    def step_once(self):
        """
        Advance exactly one yielded Step without scheduling further steps.
        Useful for single-step demo mode.
        """
        # If there is no iterator or it's running continuously, do nothing (caller should pause first).
        if self._iter is None:
            return
        try:
            step: Step = next(self._iter)
            self.canvas_view.draw_bars(step.array, step.highlights)
            if self._metrics_cb:
                self._metrics_cb()
        except StopIteration:
            # finished: call finish callback if present
            self._iter = None
            if self._finish_cb:
                self._finish_cb()
