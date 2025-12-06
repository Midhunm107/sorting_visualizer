# ui/controls.py
import tkinter as tk
from tkinter import ttk

class Controls:
    """
    Controls component:
    on_generate(size)
    on_start(alg_name)
    on_pause()
    on_resume()
    on_reset()
    on_speed_change(ms)
    on_size_change(size)
    on_step()  # new: single-step callback
    """

    def __init__(self, master,
                 alg_names,
                 on_generate,
                 on_start,
                 on_pause,
                 on_resume,
                 on_reset,
                 on_speed_change,
                 on_size_change,
                 on_step):
        self.frame = tk.Frame(master)
        # fonts
        label_font = ("Arial", 10)
        btn_font = ("Arial", 10)

        # Left: algorithm selection
        left = tk.Frame(self.frame)
        left.pack(side="left", padx=8)
        tk.Label(left, text="Algorithm", font=label_font).pack(anchor="w")
        self.alg_var = tk.StringVar(value=alg_names[0] if alg_names else "")
        self.alg_dropdown = ttk.Combobox(left, textvariable=self.alg_var, values=alg_names, state="readonly", width=22)
        self.alg_dropdown.pack(pady=(2,0))

        # Middle: size and speed
        mid = tk.Frame(self.frame)
        mid.pack(side="left", padx=20)
        tk.Label(mid, text="Size", font=label_font).pack(anchor="w")
        self.size_var = tk.IntVar(value=40)
        self.size_slider = tk.Scale(mid, from_=5, to=200, orient="horizontal", variable=self.size_var,
                                    command=lambda v: on_size_change(int(v)), length=220)
        self.size_slider.pack()
        tk.Label(mid, text="Speed (ms)", font=label_font).pack(anchor="w")
        self.speed_var = tk.IntVar(value=60)
        self.speed_slider = tk.Scale(mid, from_=1, to=500, orient="horizontal", variable=self.speed_var,
                                     command=lambda v: on_speed_change(int(v)), length=220)
        self.speed_slider.pack()

        # Right: buttons and metrics
        right = tk.Frame(self.frame)
        right.pack(side="left", padx=20)
        btn_row = tk.Frame(right)
        btn_row.pack()
        self.btn_generate = tk.Button(btn_row, text="Generate", command=lambda: on_generate(self.size_var.get()), font=btn_font)
        self.btn_start = tk.Button(btn_row, text="Start", command=lambda: on_start(self.alg_var.get()), font=btn_font)
        self.btn_step = tk.Button(btn_row, text="Step", command=on_step, font=btn_font)
        self.btn_pause = tk.Button(btn_row, text="Pause", command=on_pause, font=btn_font)
        self.btn_resume = tk.Button(btn_row, text="Resume", command=on_resume, font=btn_font)
        self.btn_reset = tk.Button(btn_row, text="Reset", command=on_reset, font=btn_font)
        for b in (self.btn_generate, self.btn_start, self.btn_step, self.btn_pause, self.btn_resume, self.btn_reset):
            b.pack(side="left", padx=3, pady=2)

        # metrics label
        self.metrics_label = tk.Label(right, text="Comparisons: 0    Swaps: 0    Time: 0.000s", font=("Arial", 10))
        self.metrics_label.pack(pady=(6,0))

    def disable_while_running(self):
        self.alg_dropdown.configure(state="disabled")
        self.btn_generate.configure(state="disabled")
        self.btn_start.configure(state="disabled")
        self.size_slider.configure(state="disabled")
        self.btn_step.configure(state="disabled")  # disable stepping while continuous running

    def enable_all(self):
        self.alg_dropdown.configure(state="readonly")
        self.btn_generate.configure(state="normal")
        self.btn_start.configure(state="normal")
        self.size_slider.configure(state="normal")
        self.btn_step.configure(state="normal")

    def enable_stepping_only(self):
        """
        Called when paused: allow user to click Step but disallow Generate/Start to avoid state conflict.
        """
        self.alg_dropdown.configure(state="disabled")
        self.btn_generate.configure(state="disabled")
        self.btn_start.configure(state="disabled")
        self.size_slider.configure(state="disabled")
        self.btn_step.configure(state="normal")

    def update_metrics_display(self, metrics):
        self.metrics_label.config(text=f"Comparisons: {metrics.comparisons}    Swaps: {metrics.swaps}    Time: {metrics.time:.3f}s")
