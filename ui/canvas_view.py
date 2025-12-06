# ui/canvas_view.py
import tkinter as tk

class CanvasView(tk.Canvas):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.last_drawn = None
        self.configure(highlightthickness=0)  # remove border highlight
        self.bind("<Configure>", self._on_resize)

    def _on_resize(self, event):
        # redraw last array on resize for consistent visuals
        if self.last_drawn:
            arr, highlights = self.last_drawn
            # avoid too small redraws
            try:
                self.draw_bars(arr, highlights)
            except Exception:
                pass

    def draw_bars(self, array, highlights):
        """
        Draw vertical bars with a small gap between them to make boundaries visible.
        highlights: dict index->color
        """
        self.delete("all")
        # keep a copy of last state for redraw on resize
        self.last_drawn = (array[:] if array else [], highlights.copy() if highlights else {})

        w = self.winfo_width() or 800
        h = self.winfo_height() or 360
        n = len(array) if array else 0
        if n == 0:
            return

        # compute bar width with a small gap
        total_gap = max(1, int(n * 0.15))  # proportional total gap pixels
        base_bar_w = w / max(1, n)
        gap = min(4, max(1, int(base_bar_w * 0.12)))  # small gap proportional to width
        bar_w = max(1, base_bar_w - gap)

        max_v = max(array) if array else 1
        for i, val in enumerate(array):
            x0 = i * (bar_w + gap)
            x1 = x0 + bar_w
            # ensure we don't draw outside canvas width
            if x0 >= w:
                break
            y1 = h
            y0 = h - (val / max_v) * (h - 20)
            color = highlights.get(i, "gray")
            # create rectangle with no outline for smoother look
            self.create_rectangle(x0 + 1, y0, x1 - 1, y1, fill=color, outline="")
