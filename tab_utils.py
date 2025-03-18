import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
import psutil
import wmi

def create_monitor_tab(self, parent):
    main_frame = ttk.Frame(parent)
    main_frame.grid(row=0, column=0, sticky="nsew")
    parent.grid_columnconfigure(0, weight=1)
    parent.grid_rowconfigure(0, weight=1)

    # Left Panel - System Stats (สมมติว่ามีฟังก์ชันนี้แยกไปด้วย)
    self.create_left_panel(main_frame)

    # Right Panel - Tools & Info
    right_panel = ttk.Frame(main_frame)
    right_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

    # Configure right panel grid
    right_panel.grid_columnconfigure(0, weight=1)
    right_panel.grid_rowconfigure(1, weight=1)

    # Tools Section
    tools_frame = ttk.LabelFrame(right_panel, text="System Tools", padding=20)
    tools_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
    tools_frame.grid_columnconfigure(0, weight=1)

    # Benchmark Card
    benchmark_frame = ttk.Frame(tools_frame)
    benchmark_frame.grid(row=0, column=0, sticky="ew", pady=8)

    ttk.Label(
        benchmark_frame,
        text="🔍 System Benchmark",
        font=("Segoe UI", 13, "bold"),
        foreground="#2c3e50",
    ).grid(row=0, column=0, sticky="w")

    benchmark_controls = ttk.Frame(benchmark_frame)
    benchmark_controls.grid(row=1, column=0, sticky="ew", pady=5)

    self.stress_duration = ttk.Entry(benchmark_controls, width=10, style='TEntry')
    self.stress_duration.insert(0, "30")
    self.stress_duration.grid(row=0, column=0, padx=5)

    ttk.Label(benchmark_controls, text="seconds", foreground="#2c3e50").grid(row=0, column=1, padx=5)

    self.start_benchmark_btn = ttk.Button(
        benchmark_controls,
        text="Start Benchmark",
        command=self.start_benchmark,
        style='primary.TButton'
    )
    self.start_benchmark_btn.grid(row=0, column=2, padx=5)

    self.benchmark_status = ttk.Label(
        benchmark_frame,
        text="Ready to benchmark",
        font=("Segoe UI", 10),
        foreground="#27ae60",
    )
    self.benchmark_status.grid(row=2, column=0, pady=5)

    # System Info Card
    info_frame = ttk.LabelFrame(right_panel, text="System Information", padding=15)
    info_frame.grid(row=1, column=0, sticky="nsew")

    self.info_text = tk.Text(info_frame, height=10, bg='#f0f0f0', fg='#2c3e50', font=("Consolas", 10), wrap=tk.WORD, relief=tk.FLAT)
    self.info_text.grid(row=0, column=0, sticky="nsew")

def create_pg_test_tab(self, parent):
    container = ttk.Frame(parent)
    container.place(relx=0.5, rely=0.5, anchor="center")

    result_frame = ttk.LabelFrame(container, text="Test Results", padding=10)
    result_frame.pack(fill='x', pady=(0, 10))

    self.pg_result_text = tk.Text(result_frame, height=4, width=60)
    self.pg_result_text.pack(padx=5, pady=5)

    control_frame = ttk.Frame(container)
    control_frame.pack(fill='x')

    selection_frame = ttk.Frame(control_frame)
    selection_frame.pack(fill='x', pady=10)

    cpu_btn = ttk.Radiobutton(
        selection_frame,
        text="Use CPU",
        variable=self.pg_test_device,
        value='cpu',
        style='primary.TRadiobutton'
    )
    cpu_btn.pack(side='left', padx=5)

    gpu_btn = ttk.Radiobutton(
        selection_frame,
        text="Use GPU",
        variable=self.pg_test_device,
        value='gpu',
        style='primary.TRadiobutton'
    )
    gpu_btn.pack(side='left', padx=5)

    start_btn = ttk.Button(
        control_frame,
        text="Start Program Tests",
        command=self.start_pg_tests,
        style='primary.TButton',
        width=20
    )
    start_btn.pack(pady=10)

    self.pg_tests = {
        "Matrix Multiplication": {"progress": None, "score": None, "desc": "ทดสอบการคำนวณเมทริกซ์ขนาดใหญ่", "time": None},
        "File Operations": {"progress": None, "score": None, "desc": "ทดสอบการอ่านเขียนไฟล์", "time": None},
        "String Processing": {"progress": None, "score": None, "desc": "ทดสอบการประมวลผลข้อความ", "time": None},
        "Data Sorting": {"progress": None, "score": None, "desc": "ทดสอบการเรียงลำดับข้อมูล", "time": None},
        "Image Processing": {"progress": None, "score": None, "desc": "ทดสอบการประมวลผลภาพ", "time": None}
    }

    for test_name, test_data in self.pg_tests.items():
        test_frame = ttk.LabelFrame(control_frame, text=test_name, padding=10)
        test_frame.pack(fill='x', pady=5)

        desc_frame = ttk.Frame(test_frame)
        desc_frame.pack(fill='x', pady=(0, 5))

        desc_label = ttk.Label(desc_frame, text=test_data["desc"], font=("Segoe UI", 10))
        desc_label.pack(side='left')

        progress_frame = ttk.Frame(test_frame)
        progress_frame.pack(fill='x')

        progress = ttk.Progressbar(progress_frame, length=400, mode='determinate', style='primary.Horizontal.TProgressbar')
        progress.pack(side='left', expand=True, fill='x', padx=(0, 10))
        test_data["progress"] = progress

        info_frame = ttk.Frame(progress_frame)
        info_frame.pack(side='right')

        time_label = ttk.Label(info_frame, text="Time: 0.00s", font=("Segoe UI", 10))
        time_label.pack(side='left', padx=5)
        test_data["time"] = time_label

        score_label = ttk.Label(info_frame, text="Score: 0%", font=("Segoe UI", 10))
        score_label.pack(side='left', padx=5)
        test_data["score"] = score_label

def create_ai_test_tab(self, parent):
    container = ttk.Frame(parent)
    container.place(relx=0.5, rely=0.5, anchor="center")

    result_frame = ttk.LabelFrame(container, text="Test Results", padding=10)
    result_frame.pack(fill='x', pady=(0, 10))

    self.ai_result_text = tk.Text(result_frame, height=4, width=60)
    self.ai_result_text.pack(padx=5, pady=5)

    control_frame = ttk.Frame(container)
    control_frame.pack(fill='x')

    selection_frame = ttk.Frame(control_frame)
    selection_frame.pack(fill='x', pady=10)

    cpu_btn = ttk.Radiobutton(
        selection_frame,
        text="Use CPU",
        variable=self.ai_test_device,
        value='cpu',
        style='primary.TRadiobutton'
    )
    cpu_btn.pack(side='left', padx=5)

    gpu_btn = ttk.Radiobutton(
        selection_frame,
        text="Use GPU",
        variable=self.ai_test_device,
        value='gpu',
        style='primary.TRadiobutton'
    )
    gpu_btn.pack(side='left', padx=5)

    start_btn = ttk.Button(
        control_frame,
        text="Start AI Tests",
        command=self.start_ai_tests,
        style='primary.TButton',
        width=20
    )
    start_btn.pack(pady=10)

    self.ai_tests = {
        "Neural Network": {"progress": None, "score": None, "desc": "ทดสอบการเทรนโมเดล Neural Network", "time": None},
        "Image Recognition": {"progress": None, "score": None, "desc": "ทดสอบการรู้จำภาพ", "time": None},
        "Natural Language": {"progress": None, "score": None, "desc": "ทดสอบการประมวลผลภาษาธรรมชาติ", "time": None},
        "Data Classification": {"progress": None, "score": None, "desc": "ทดสอบการจำแนกข้อมูล", "time": None},
        "Clustering": {"progress": None, "score": None, "desc": "ทดสอบการจัดกลุ่มข้อมูลด้วย AI", "time": None}
    }

    for test_name, test_data in self.ai_tests.items():
        test_frame = ttk.LabelFrame(control_frame, text=test_name, padding=10)
        test_frame.pack(fill='x', pady=5)

        desc_frame = ttk.Frame(test_frame)
        desc_frame.pack(fill='x', pady=(0, 5))

        desc_label = ttk.Label(
            desc_frame,
            text=test_data["desc"],
            font=("Segoe UI", 10)
        )
        desc_label.pack(side='left')

        progress_frame = ttk.Frame(test_frame)
        progress_frame.pack(fill='x')

        progress = ttk.Progressbar(
            progress_frame,
            length=400,
            mode='determinate',
            style='primary.Horizontal.TProgressbar'
        )
        progress.pack(side='left', expand=True, fill='x', padx=(0, 10))
        test_data["progress"] = progress

        info_frame = ttk.Frame(progress_frame)
        info_frame.pack(side='right')

        time_label = ttk.Label(
            info_frame,
            text="Time: 0.00s",
            font=("Segoe UI", 10)
        )
        time_label.pack(side='left', padx=5)
        test_data["time"] = time_label

        score_label = ttk.Label(
            info_frame,
            text="Score: 0%",
            font=("Segoe UI", 10)
        )
        score_label.pack(side='left', padx=5)
        test_data["score"] = score_label

def create_hardware_tab(self, parent):
    main_frame = ttk.Frame(parent, padding="20")
    main_frame.pack(fill=tk.BOTH, expand=True)

    left_column = ttk.Frame(main_frame)
    right_column = ttk.Frame(main_frame)
    left_column.pack(side="left", fill="both", expand=True, padx=(0, 10))
    right_column.pack(side="right", fill="both", expand=True, padx=(10, 0))

    computer = wmi.WMI()
    system_info = computer.Win32_ComputerSystem()[0]
    os_info = computer.Win32_OperatingSystem()[0]
    cpu_info = computer.Win32_Processor()[0]
    bios = computer.Win32_BIOS()[0]
    board = computer.Win32_BaseBoard()[0]
    memory_info = computer.Win32_PhysicalMemory()
    disk_info = computer.Win32_DiskDrive()
    
    try:
        nvidia_smi = subprocess.check_output(["nvidia-smi", "--query-gpu=name,memory.total,utilization.gpu", "--format=csv,noheader,nounits"]).decode()
        gpu_name, gpu_memory, gpu_load = nvidia_smi.strip().split(", ")
        gpu_memory = f"{float(gpu_memory):.0f} MB"
        gpu_load = f"{float(gpu_load):.1f}%"
    except:
        try:
            gpu = computer.Win32_VideoController()[0]
            gpu_name = gpu.Name
            gpu_memory = f"{int(gpu.AdapterRAM / (1024*1024)):.0f} MB" if gpu.AdapterRAM else "N/A"
            gpu_load = "N/A"
        except:
            gpu_name = "N/A"
            gpu_memory = "N/A"
            gpu_load = "N/A"

    left_sections = [
        ("🖥️ System Information", [
            ("Manufacturer", system_info.Manufacturer),
            ("Model", system_info.Model),
            ("System Type", system_info.SystemType),
            ("Total Physical Memory", f"{round(float(os_info.TotalVisibleMemorySize) / 1024 / 1024, 2)} GB"),
            ("OS Version", os_info.Caption),
            ("OS Architecture", os_info.OSArchitecture),
        ]),
        ("⚡ Processor (CPU)", [
            ("Name", cpu_info.Name.strip()),
            ("Manufacturer", cpu_info.Manufacturer),
            ("Cores", cpu_info.NumberOfCores),
            ("Threads", cpu_info.NumberOfLogicalProcessors),
            ("Base Speed", f"{cpu_info.MaxClockSpeed} MHz"),
            ("Socket", cpu_info.SocketDesignation),
            ("Architecture", cpu_info.Architecture),
            ("L2 Cache", f"{cpu_info.L2CacheSize} KB" if cpu_info.L2CacheSize else "N/A"),
            ("L3 Cache", f"{cpu_info.L3CacheSize} KB" if cpu_info.L3CacheSize else "N/A"),
        ]),
        ("🎮 Graphics Card (GPU)", [
            ("Name", gpu_name),
            ("Total Memory", gpu_memory),
            ("Current Load", gpu_load),
        ]),
    ]

    right_sections = [
        ("📟 Motherboard", [
            ("Manufacturer", board.Manufacturer),
            ("Product", board.Product),
            ("Serial Number", board.SerialNumber),
            ("BIOS Version", bios.Version),
            ("BIOS Vendor", bios.Manufacturer),
            ("BIOS Release Date", bios.ReleaseDate.split(".")[0] if hasattr(bios, "ReleaseDate") else "N/A"),
        ]),
        ("💾 Memory (RAM)", [
            (f"Slot {i+1}", f"{int(float(m.Capacity) / 1024 / 1024 / 1024)} GB {m.Speed} MHz {m.Manufacturer}")
            for i, m in enumerate(memory_info)
        ]),
        ("💿 Storage", [
            (f"{d.Model}", f"{round(float(d.Size) / 1024 / 1024 / 1024, 2)} GB")
            for d in disk_info
        ]),
    ]

    # Populate left column
    for title, items in left_sections:
        frame = ttk.LabelFrame(left_column, text=title, padding=10)
        frame.pack(fill="x", pady=5)
        for label, value in items:
            ttk.Label(frame, text=f"{label}: {value}", font=("Segoe UI", 10)).pack(anchor="w")

    # Populate right column
    for title, items in right_sections:
        frame = ttk.LabelFrame(right_column, text=title, padding=10)
        frame.pack(fill="x", pady=5)
        for label, value in items:
            ttk.Label(frame, text=f"{label}: {value}", font=("Segoe UI", 10)).pack(anchor="w")