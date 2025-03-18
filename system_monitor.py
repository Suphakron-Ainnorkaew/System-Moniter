import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
import threading
from tab_utils import create_monitor_tab, create_pg_test_tab, create_ai_test_tab, create_hardware_tab
from gui_utils import create_sections, create_left_panel, create_stat_card, create_menu
from benchmark_utils import start_benchmark, run_stress_test
from system_info_utils import update_system_info, get_gpu_usage, get_gpu_memory, get_gpu_total_memory, get_gpu_temperature, check_ai_capability, get_gpu_count, get_gpu_name
from test_utils import update_test_progress, start_pg_tests, start_ai_tests
from history_utils import view_logs, view_benchmark_history
from system_monitor_db import SystemMonitorDB

class SystemMonitorApp:
    def __init__(self, master):
        self.pg_test_device = tk.StringVar(value='cpu')
        self.ai_test_device = tk.StringVar(value='cpu')
        self.db = SystemMonitorDB()

        self.master = master
        self.style = ttk.Style(theme='flatly')
        master.title("System Monitor Pro")
        master.geometry("1200x800")
        master.configure(bg='#ffffff')

        self.style.configure('TNotebook.Tab', padding=[20, 10], font=('Segoe UI', 11))
        self.style.configure('TLabelframe.Label', font=('Segoe UI', 12, 'bold'), foreground='#2c3e50')
        self.style.configure('Header.TLabel', font=('Segoe UI', 18, 'bold'), foreground='#2c3e50')
        self.style.configure('Status.TLabel', font=('Segoe UI', 11))
        self.style.configure('Card.TFrame', background='#ffffff', relief='solid', borderwidth=1)
        self.style.configure('CPU.Horizontal.TProgressbar', foreground='#3498db', background='#3498db')
        self.style.configure('GPU.Horizontal.TProgressbar', foreground='#e74c3c', background='#e74c3c')
        self.style.configure('RAM.Horizontal.TProgressbar', foreground='#2ecc71', background='#2ecc71')
        self.style.configure('Storage.Horizontal.TProgressbar', foreground='#f1c40f', background='#f1c40f')

        self.monitoring = True
        self.is_benchmarking = False
        self.benchmark_data = {'cpu_max': 0, 'gpu_max': 0, 'memory_max': 0, 'start_time': 0}

        self.main_notebook = ttk.Notebook(master)
        self.main_notebook.pack(fill='both', expand=True, padx=10, pady=10)

        self.monitor_frame = ttk.Frame(self.main_notebook)
        self.pg_frame = ttk.Frame(self.main_notebook)
        self.ai_frame = ttk.Frame(self.main_notebook)
        self.hw_frame = ttk.Frame(self.main_notebook)

        self.main_notebook.add(self.monitor_frame, text=" 🖥️ System Monitor ")
        self.main_notebook.add(self.pg_frame, text=" 💻 Program Test ")
        self.main_notebook.add(self.ai_frame, text=" 🤖 AI Test ")
        self.main_notebook.add(self.hw_frame, text=" 🔧 Hardware Info ")

        create_monitor_tab(self, self.monitor_frame)
        create_pg_test_tab(self, self.pg_frame)
        create_ai_test_tab(self, self.ai_frame)
        create_hardware_tab(self, self.hw_frame)

        create_menu(self)

        # เริ่มการ мониторинг ระบบใน thread แยก
        self.monitor_thread = threading.Thread(target=update_system_info, args=(self,))
        self.monitor_thread.daemon = True
        self.monitor_thread.start()

        try:
            icon = tk.PhotoImage(file="BML.png")
            self.master.iconphoto(True, icon)
        except Exception as e:
            print(f"Error loading icon: {e}")

        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    # Bind methods from utils
    create_sections = create_sections
    create_left_panel = create_left_panel
    create_stat_card = create_stat_card
    start_benchmark = start_benchmark
    run_stress_test = run_stress_test
    update_system_info = update_system_info
    get_gpu_usage = get_gpu_usage
    get_gpu_memory = get_gpu_memory
    get_gpu_total_memory = get_gpu_total_memory
    get_gpu_temperature = get_gpu_temperature
    check_ai_capability = check_ai_capability
    get_gpu_count = get_gpu_count
    get_gpu_name = get_gpu_name
    update_test_progress = update_test_progress
    start_pg_tests = start_pg_tests
    start_ai_tests = start_ai_tests
    view_logs = view_logs
    view_benchmark_history = view_benchmark_history

    def on_closing(self):
        self.monitoring = False
        self.master.destroy()
        

def main():
    root = tk.Tk()
    app = SystemMonitorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()