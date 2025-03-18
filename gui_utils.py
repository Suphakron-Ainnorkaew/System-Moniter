import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk

def create_sections(parent, sections):
    canvas = tk.Canvas(parent, highlightthickness=0)
    scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    for section_title, items in sections:
        section_frame = ttk.LabelFrame(scrollable_frame, text=section_title, padding="15")
        section_frame.pack(fill="x", padx=5, pady=5)

        for j, (label, value) in enumerate(items):
            label_widget = ttk.Label(
                section_frame,
                text=label + ":",
                font=("Segoe UI", 10, "bold"),
                foreground="#2c3e50"
            )
            label_widget.grid(row=j, column=0, sticky="w", padx=5, pady=3)
            
            value_widget = ttk.Label(
                section_frame,
                text=str(value),
                font=("Segoe UI", 10),
                foreground="#34495e"
            )
            value_widget.grid(row=j, column=1, sticky="w", padx=5, pady=3)

        section_frame.grid_columnconfigure(1, weight=1)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

def create_left_panel(self, main_frame):
    left_panel = ttk.Frame(main_frame)
    left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

    left_panel.grid_columnconfigure(0, weight=1)
    for i in range(4):
        left_panel.grid_rowconfigure(i, weight=1)

    self.create_stat_card(left_panel, "CPU Usage", "cpu", 0)
    self.create_stat_card(left_panel, "GPU Usage", "gpu", 1)
    self.create_stat_card(left_panel, "RAM Usage", "ram", 2)
    self.create_stat_card(left_panel, "Storage Usage", "storage", 3)

def create_stat_card(self, parent, title, type_, row):
    card = ttk.Frame(parent, style='Card.TFrame')
    card.grid(row=row, column=0, sticky="nsew", pady=5, padx=10)

    card.grid_columnconfigure(0, weight=1)
    card.configure(padding=15)

    icon_map = {
        "cpu": "🔲",
        "gpu": "📊",
        "memory": "💾",
        "ram": "📈",
        "storage": "💻"
    }

    title_frame = ttk.Frame(card)
    title_frame.grid(row=0, column=0, sticky="ew", pady=(0, 8))
    title_frame.grid_columnconfigure(0, weight=1)

    ttk.Label(
        title_frame,
        text=f"{icon_map.get(type_, '📈')} {title}",
        font=("Segoe UI", 12, "bold"),
        foreground="#2c3e50"
    ).grid(row=0, column=0, sticky="w")

    if type_ == "cpu":
        value_frame = ttk.Frame(card)
        value_frame.grid(row=1, column=0, sticky="ew")
        value_frame.grid_columnconfigure(0, weight=1)

        self.cpu_percent = ttk.Label(value_frame, text="0%", font=("Segoe UI", 20, "bold"), foreground="#3498db")
        self.cpu_percent.grid(row=0, column=0)

        self.cpu_temp = ttk.Label(value_frame, text="Temperature: 0°C", font=("Segoe UI", 10), foreground="#7f8c8d")
        self.cpu_temp.grid(row=1, column=0)

        progress_frame = ttk.Frame(card)
        progress_frame.grid(row=2, column=0, sticky="ew", pady=(8, 0))
        progress_frame.grid_columnconfigure(0, weight=1)

        self.cpu_progress = ttk.Progressbar(progress_frame, mode='determinate', style='CPU.Horizontal.TProgressbar')
        self.cpu_progress.grid(row=0, column=0, sticky="ew")

    elif type_ == "gpu":
        value_frame = ttk.Frame(card)
        value_frame.grid(row=1, column=0, sticky="ew")
        value_frame.grid_columnconfigure(0, weight=1)

        self.gpu_percent = ttk.Label(value_frame, text="0%", font=("Segoe UI", 20, "bold"), foreground="#e74c3c")
        self.gpu_percent.grid(row=0, column=0)

        self.gpu_memory = ttk.Label(value_frame, text="Memory: 0/0 MB", font=("Segoe UI", 10), foreground="#7f8c8d")
        self.gpu_memory.grid(row=1, column=0)

        progress_frame = ttk.Frame(card)
        progress_frame.grid(row=2, column=0, sticky="ew", pady=(8, 0))
        progress_frame.grid_columnconfigure(0, weight=1)

        self.gpu_progress = ttk.Progressbar(progress_frame, mode='determinate', style='GPU.Horizontal.TProgressbar')
        self.gpu_progress.grid(row=0, column=0, sticky="ew")

    elif type_ == "ram":
        value_frame = ttk.Frame(card)
        value_frame.grid(row=1, column=0, sticky="ew")
        value_frame.grid_columnconfigure(0, weight=1)

        self.ram_percent = ttk.Label(value_frame, text="0%", font=("Segoe UI", 20, "bold"), foreground="#4CAF50")
        self.ram_percent.grid(row=0, column=0)

        self.total_ram = ttk.Label(value_frame, text="Total: 0 GB", font=("Segoe UI", 10), foreground="#7f8c8d")
        self.total_ram.grid(row=1, column=0)

        progress_frame = ttk.Frame(card)
        progress_frame.grid(row=2, column=0, sticky="ew", pady=(8, 0))
        progress_frame.grid_columnconfigure(0, weight=1)

        self.ram_progress = ttk.Progressbar(progress_frame, mode='determinate', style='RAM.Horizontal.TProgressbar')
        self.ram_progress.grid(row=0, column=0, sticky="ew")

    elif type_ == "storage":
        value_frame = ttk.Frame(card)
        value_frame.grid(row=1, column=0, sticky="ew")
        value_frame.grid_columnconfigure(0, weight=1)

        self.storage_percent = ttk.Label(value_frame, text="0%", font=("Segoe UI", 20, "bold"), foreground="#FF9800")
        self.storage_percent.grid(row=0, column=0)

        self.total_storage = ttk.Label(value_frame, text="Total: 0 GB", font=("Segoe UI", 10), foreground="#7f8c8d")
        self.total_storage.grid(row=1, column=0)

        progress_frame = ttk.Frame(card)
        progress_frame.grid(row=2, column=0, sticky="ew", pady=(8, 0))
        progress_frame.grid_columnconfigure(0, weight=1)

        self.storage_progress = ttk.Progressbar(progress_frame, mode='determinate', style='Storage.Horizontal.TProgressbar')
        self.storage_progress.grid(row=0, column=0, sticky="ew")

def create_menu(self):
    menubar = tk.Menu(self.master)
    self.master.config(menu=menubar)

    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="View Logs", command=self.view_logs)
    file_menu.add_command(label="View Benchmark History", command=self.view_benchmark_history)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=self.on_closing)