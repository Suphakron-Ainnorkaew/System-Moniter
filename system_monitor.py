import tkinter as tk
from ttkbootstrap import ttk, Style
import psutil
import wmi
import threading
import time
import logging
import traceback
import os
from datetime import datetime
import platform
import csv
from gui_utils import GUIUtils
from tab_utils import TabUtils
from system_monitor_db import SystemMonitorDB

# ตั้งค่า logging
logging.basicConfig(filename='system_monitor.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')

class SystemMonitorApp:
    def __init__(self, root):
        print("Starting System Monitor Application...")
        self.root = root
        self.root.title("🖥️ System Performance Monitor")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Set app icon and theme
        self.style = Style('cosmo')  # Modern theme
        self.setup_styles()
        
        self.db = SystemMonitorDB()
        self.gui_utils = GUIUtils(self)
        self.tab_utils = TabUtils(self)
        
        # Initialize monitoring variables
        self.cpu_history = []
        self.memory_history = []
        self.disk_history = []
        self.network_history = []
        self.max_history = 60  # Keep 60 data points
        self.update_interval = 1000  # Default update interval in ms
        
        self.create_gui()
        self.update_system_info()

    def setup_styles(self):
        """ตั้งค่า modern styles"""
        try:
            self.style.configure('Card.TFrame',
                               relief='flat',
                               borderwidth=2,
                               background='#ffffff')
            
            self.style.configure('Header.TLabel',
                               font=('Segoe UI', 18, 'bold'),
                               foreground='#2c3e50',
                               background='#ffffff')
            
            self.style.configure('Subheader.TLabel',
                               font=('Segoe UI', 12, 'bold'),
                               foreground='#34495e',
                               background='#ffffff')
            
            self.style.configure('Value.TLabel',
                               font=('Segoe UI', 24, 'bold'),
                               foreground='#e74c3c',
                               background='#ffffff')
            
            self.style.configure('Info.TLabel',
                               font=('Segoe UI', 11),
                               foreground='#7f8c8d',
                               background='#ffffff')
            
            self.style.configure('Status.TLabel',
                               font=('Segoe UI', 10, 'bold'),
                               background='#ffffff')
            
            self.style.configure('Compact.TButton',
                               font=('Segoe UI', 9),
                               padding=(12, 6))
            
        except Exception as e:
            logging.error(f"Error setting up styles: {e}")

    def create_gui(self):
        try:
            logging.debug("Creating GUI")
            
            main_container = ttk.Frame(self.root)
            main_container.pack(fill='both', expand=True, padx=15, pady=15)
            
            self.notebook = ttk.Notebook(main_container)
            self.notebook.pack(expand=True, fill='both')
            
            self.system_monitor_frame = ttk.Frame(self.notebook)
            self.ai_test_frame = ttk.Frame(self.notebook)
            self.pg_test_frame = ttk.Frame(self.notebook)
            
            self.notebook.add(self.system_monitor_frame, text='🖥️ System Monitor')
            self.notebook.add(self.ai_test_frame, text='🤖 AI Test')
            self.notebook.add(self.pg_test_frame, text='⚙️ Program Test')
            
            self.create_system_monitor_tab()
            self.tab_utils.create_ai_test_tab(self.ai_test_frame)
            self.tab_utils.create_pg_test_tab(self.pg_test_frame)
            
            self.create_menu()
            self.create_status_bar()
            
        except Exception as e:
            error_msg = f"Error creating GUI: {str(e)}"
            logging.error(error_msg + f"\n{traceback.format_exc()}")
            print(error_msg + f"\n{traceback.format_exc()}")

    def create_system_monitor_tab(self):
        try:
            for widget in self.system_monitor_frame.winfo_children():
                widget.destroy()
            
            canvas = tk.Canvas(self.system_monitor_frame, bg='#f8f9fa')
            scrollbar = ttk.Scrollbar(self.system_monitor_frame, orient='vertical', command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas)
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            def _on_mousewheel(event):
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
            
            self.create_header_section(scrollable_frame)
            self.create_system_info_cards(scrollable_frame)
            self.create_performance_metrics(scrollable_frame)
            self.create_system_details(scrollable_frame)
            self.create_network_processes_section(scrollable_frame)
            
        except Exception as e:
            error_msg = f"Error creating system monitor tab: {str(e)}"
            logging.error(error_msg + f"\n{traceback.format_exc()}")
            print(error_msg + f"\n{traceback.format_exc()}")

    def create_header_section(self, parent):
        header_frame = ttk.Frame(parent, style='Card.TFrame')
        header_frame.pack(fill='x', padx=20, pady=(20, 10))
        
        title_label = ttk.Label(header_frame, 
                               text="🖥️ System Performance Monitor",
                               style='Header.TLabel')
        title_label.pack(pady=(15, 5))
        
        self.time_label = ttk.Label(header_frame, 
                                   text="",
                                   style='Info.TLabel')
        self.time_label.pack(pady=(0, 15))
        
        separator = ttk.Separator(header_frame, orient='horizontal')
        separator.pack(fill='x', padx=20, pady=(5, 10))

    def create_system_info_cards(self, parent):
        cards_frame = ttk.Frame(parent)
        cards_frame.pack(fill='x', padx=20, pady=10)
        
        top_row = ttk.Frame(cards_frame)
        top_row.pack(fill='x', pady=(0, 10))
        
        cpu_card = self.create_metric_card(top_row, "🔥 CPU Usage", "0.0%", "#e74c3c")
        cpu_card.pack(side='left', fill='both', expand=True, padx=(0, 10))
        self.cpu_label = cpu_card.children['!label2']
        self.cpu_progress = cpu_card.children['!progressbar']
        
        memory_card = self.create_metric_card(top_row, "🧠 Memory Usage", "0.0%", "#3498db")
        memory_card.pack(side='left', fill='both', expand=True, padx=(0, 10))
        self.memory_label = memory_card.children['!label2']
        self.memory_progress = memory_card.children['!progressbar']
        
        disk_card = self.create_metric_card(top_row, "💾 Disk Usage", "0.0%", "#f39c12")
        disk_card.pack(side='left', fill='both', expand=True)
        self.disk_label = disk_card.children['!label2']
        self.disk_progress = disk_card.children['!progressbar']
        
        bottom_row = ttk.Frame(cards_frame)
        bottom_row.pack(fill='x')
        
        network_card = self.create_info_card(bottom_row, "🌐 Network", "Monitoring...")
        network_card.pack(side='left', fill='both', expand=True, padx=(0, 10))
        self.network_label = network_card.children['!label2']
        
        temp_card = self.create_info_card(bottom_row, "🌡️ Temperature", "N/A")
        temp_card.pack(side='left', fill='both', expand=True, padx=(0, 10))
        self.temp_label = temp_card.children['!label2']
        
        uptime_card = self.create_info_card(bottom_row, "⏰ Uptime", "Calculating...")
        uptime_card.pack(side='left', fill='both', expand=True)
        self.uptime_label = uptime_card.children['!label2']

    def create_metric_card(self, parent, title, value, color):
        card = ttk.Frame(parent, style='Card.TFrame', padding=15)
        
        title_label = ttk.Label(card, text=title, style='Subheader.TLabel')
        title_label.pack(anchor='w')
        
        value_label = ttk.Label(card, text=value, style='Value.TLabel')
        value_label.pack(anchor='w', pady=(5, 10))
        
        progress = ttk.Progressbar(card, length=200, mode='determinate', style=f"{color}.Horizontal.TProgressbar")
        progress.pack(fill='x', pady=(0, 5))
        
        return card

    def create_info_card(self, parent, title, value):
        card = ttk.Frame(parent, style='Card.TFrame', padding=15)
        
        title_label = ttk.Label(card, text=title, style='Subheader.TLabel')
        title_label.pack(anchor='w')
        
        value_label = ttk.Label(card, text=value, style='Info.TLabel')
        value_label.pack(anchor='w', pady=(5, 0))
        
        return card

    def create_performance_metrics(self, parent):
        metrics_frame = ttk.LabelFrame(parent, text="📊 Performance Metrics", padding=15)
        metrics_frame.pack(fill='x', padx=20, pady=10)
        
        grid_frame = ttk.Frame(metrics_frame)
        grid_frame.pack(fill='x')
        
        left_col = ttk.Frame(grid_frame)
        left_col.pack(side='left', fill='both', expand=True, padx=(0, 20))
        
        cpu_frame = ttk.LabelFrame(left_col, text="🔥 CPU Details", padding=10)
        cpu_frame.pack(fill='x', pady=(0, 10))
        
        self.cpu_count_label = ttk.Label(cpu_frame, text="Cores: Detecting...", style='Info.TLabel')
        self.cpu_count_label.pack(anchor='w')
        
        self.cpu_freq_label = ttk.Label(cpu_frame, text="Frequency: Detecting...", style='Info.TLabel')
        self.cpu_freq_label.pack(anchor='w')
        
        self.cpu_temp_label = ttk.Label(cpu_frame, text="Temperature: N/A", style='Info.TLabel')
        self.cpu_temp_label.pack(anchor='w')
        
        memory_frame = ttk.LabelFrame(left_col, text="🧠 Memory Details", padding=10)
        memory_frame.pack(fill='x')
        
        self.memory_total_label = ttk.Label(memory_frame, text="Total: Detecting...", style='Info.TLabel')
        self.memory_total_label.pack(anchor='w')
        
        self.memory_available_label = ttk.Label(memory_frame, text="Available: Detecting...", style='Info.TLabel')
        self.memory_available_label.pack(anchor='w')
        
        self.memory_used_label = ttk.Label(memory_frame, text="Used: Detecting...", style='Info.TLabel')
        self.memory_used_label.pack(anchor='w')
        
        right_col = ttk.Frame(grid_frame)
        right_col.pack(side='left', fill='both', expand=True)
        
        disk_frame = ttk.LabelFrame(right_col, text="💾 Disk Details", padding=10)
        disk_frame.pack(fill='x', pady=(0, 10))
        
        self.disk_total_label = ttk.Label(disk_frame, text="Total: Detecting...", style='Info.TLabel')
        self.disk_total_label.pack(anchor='w')
        
        self.disk_free_label = ttk.Label(disk_frame, text="Free: Detecting...", style='Info.TLabel')
        self.disk_free_label.pack(anchor='w')
        
        self.disk_used_label = ttk.Label(disk_frame, text="Used: Detecting...", style='Info.TLabel')
        self.disk_used_label.pack(anchor='w')
        
        network_frame = ttk.LabelFrame(right_col, text="🌐 Network Details", padding=10)
        network_frame.pack(fill='x')
        
        self.network_sent_label = ttk.Label(network_frame, text="Sent: 0 MB", style='Info.TLabel')
        self.network_sent_label.pack(anchor='w')
        
        self.network_recv_label = ttk.Label(network_frame, text="Received: 0 MB", style='Info.TLabel')
        self.network_recv_label.pack(anchor='w')
        
        self.network_speed_label = ttk.Label(network_frame, text="Speed: Detecting...", style='Info.TLabel')
        self.network_speed_label.pack(anchor='w')

    def create_system_details(self, parent):
        details_frame = ttk.LabelFrame(parent, text="ℹ️ System Information", padding=15)
        details_frame.pack(fill='x', padx=20, pady=10)
        
        info_grid = ttk.Frame(details_frame)
        info_grid.pack(fill='x')
        
        left_info = ttk.Frame(info_grid)
        left_info.pack(side='left', fill='both', expand=True, padx=(0, 20))
        
        self.os_label = ttk.Label(left_info, text=f"OS: {platform.system()} {platform.release()}", style='Info.TLabel')
        self.os_label.pack(anchor='w', pady=2)
        
        self.machine_label = ttk.Label(left_info, text=f"Architecture: {platform.machine()}", style='Info.TLabel')
        self.machine_label.pack(anchor='w', pady=2)
        
        self.processor_label = ttk.Label(left_info, text=f"Processor: {platform.processor()}", style='Info.TLabel')
        self.processor_label.pack(anchor='w', pady=2)
        
        right_info = ttk.Frame(info_grid)
        right_info.pack(side='left', fill='both', expand=True)
        
        self.python_label = ttk.Label(right_info, text=f"Python: {platform.python_version()}", style='Info.TLabel')
        self.python_label.pack(anchor='w', pady=2)
        
        self.node_label = ttk.Label(right_info, text=f"Computer: {platform.node()}", style='Info.TLabel')
        self.node_label.pack(anchor='w', pady=2)
        
        self.boot_time_label = ttk.Label(right_info, text="Boot Time: Detecting...", style='Info.TLabel')
        self.boot_time_label.pack(anchor='w', pady=2)

    def create_network_processes_section(self, parent):
        section_frame = ttk.Frame(parent)
        section_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        processes_frame = ttk.LabelFrame(section_frame, text="🔝 Top Processes", padding=10)
        processes_frame.pack(fill='both', expand=True)
        
        process_list_frame = ttk.Frame(processes_frame)
        process_list_frame.pack(fill='both', expand=True)
        
        columns = ('PID', 'Name', 'CPU%', 'Memory%')
        self.process_tree = ttk.Treeview(process_list_frame, columns=columns, show='headings', height=8)
        
        self.process_tree.heading('PID', text='PID')
        self.process_tree.heading('Name', text='Process Name')
        self.process_tree.heading('CPU%', text='CPU %')
        self.process_tree.heading('Memory%', text='Memory %')
        
        self.process_tree.column('PID', width=80)
        self.process_tree.column('Name', width=200)
        self.process_tree.column('CPU%', width=100)
        self.process_tree.column('Memory%', width=100)
        
        process_scrollbar = ttk.Scrollbar(process_list_frame, orient='vertical', command=self.process_tree.yview)
        self.process_tree.configure(yscrollcommand=process_scrollbar.set)
        
        self.process_tree.pack(side='left', fill='both', expand=True)
        process_scrollbar.pack(side='right', fill='y')

    def create_menu(self):
        try:
            menubar = tk.Menu(self.root)
            
            file_menu = tk.Menu(menubar, tearoff=0)
            file_menu.add_command(label="📋 View Logs", command=self.view_logs)
            file_menu.add_separator()
            file_menu.add_command(label="⚙️ Settings", command=self.open_settings)
            file_menu.add_separator()
            file_menu.add_command(label="❌ Exit", command=self.root.quit)
            menubar.add_cascade(label="File", menu=file_menu)
            
            tools_menu = tk.Menu(menubar, tearoff=0)
            tools_menu.add_command(label="🔄 Refresh", command=self.refresh_all)
            tools_menu.add_command(label="📤 Export Data", command=self.export_data)
            tools_menu.add_command(label="🧹 Clean Cache", command=self.clean_cache)
            menubar.add_cascade(label="Tools", menu=tools_menu)
            
            help_menu = tk.Menu(menubar, tearoff=0)
            help_menu.add_command(label="❓ About", command=self.show_about)
            menubar.add_cascade(label="Help", menu=help_menu)
            
            self.root.config(menu=menubar)
            
        except Exception as e:
            error_msg = f"Error creating menu: {str(e)}"
            logging.error(error_msg + f"\n{traceback.format_exc()}")
            print(error_msg + f"\n{traceback.format_exc()}")

    def create_status_bar(self):
        self.status_frame = ttk.Frame(self.root)
        self.status_frame.pack(side='bottom', fill='x', padx=5, pady=5)
        
        self.status_label = ttk.Label(self.status_frame, text="🟢 System Monitor Ready", style='Status.TLabel')
        self.status_label.pack(side='left')
        
        self.update_label = ttk.Label(self.status_frame, text=f"⏱️ Update: {self.update_interval/1000:.1f}s", style='Status.TLabel')
        self.update_label.pack(side='right')

    def update_system_info(self):
        try:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if hasattr(self, 'time_label'):
                self.time_label.config(text=f"Last Updated: {current_time}")
            
            cpu_usage = psutil.cpu_percent(interval=0.1)
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            
            if hasattr(self, 'cpu_label'):
                self.cpu_label.config(text=f"{cpu_usage:.1f}%")
                self.cpu_progress['value'] = cpu_usage
                
            if hasattr(self, 'cpu_count_label'):
                self.cpu_count_label.config(text=f"Cores: {cpu_count} cores")
                
            if hasattr(self, 'cpu_freq_label') and cpu_freq:
                self.cpu_freq_label.config(text=f"Frequency: {cpu_freq.current:.0f} MHz")
            
            memory = psutil.virtual_memory()
            memory_usage = memory.percent
            
            if hasattr(self, 'memory_label'):
                self.memory_label.config(text=f"{memory_usage:.1f}%")
                self.memory_progress['value'] = memory_usage
                
            if hasattr(self, 'memory_total_label'):
                self.memory_total_label.config(text=f"Total: {memory.total / (1024**3):.1f} GB")
                self.memory_available_label.config(text=f"Available: {memory.available / (1024**3):.1f} GB")
                self.memory_used_label.config(text=f"Used: {memory.used / (1024**3):.1f} GB")
            
            disk_path = 'C:\\' if platform.system() == 'Windows' else '/'
            try:
                disk = psutil.disk_usage(disk_path)
                disk_usage = disk.percent
                
                if hasattr(self, 'disk_label'):
                    self.disk_label.config(text=f"{disk_usage:.1f}%")
                    self.disk_progress['value'] = disk_usage
                    
                if hasattr(self, 'disk_total_label'):
                    self.disk_total_label.config(text=f"Total: {disk.total / (1024**3):.1f} GB")
                    self.disk_free_label.config(text=f"Free: {disk.free / (1024**3):.1f} GB")
                    self.disk_used_label.config(text=f"Used: {disk.used / (1024**3):.1f} GB")
                    
            except Exception as disk_error:
                logging.error(f"Error accessing disk: {disk_error}")
            
            try:
                net_io = psutil.net_io_counters()
                if hasattr(self, 'network_sent_label'):
                    self.network_sent_label.config(text=f"Sent: {net_io.bytes_sent / (1024**2):.1f} MB")
                    self.network_recv_label.config(text=f"Received: {net_io.bytes_recv / (1024**2):.1f} MB")
            except:
                pass
            
            try:
                boot_time = datetime.fromtimestamp(psutil.boot_time())
                if hasattr(self, 'boot_time_label'):
                    self.boot_time_label.config(text=f"Boot Time: {boot_time.strftime('%Y-%m-%d %H:%M:%S')}")
            except:
                pass
            
            try:
                uptime_seconds = time.time() - psutil.boot_time()
                uptime_hours = int(uptime_seconds // 3600)
                uptime_minutes = int((uptime_seconds % 3600) // 60)
                if hasattr(self, 'uptime_label'):
                    self.uptime_label.config(text=f"{uptime_hours}h {uptime_minutes}m")
            except:
                pass
            
            self.update_processes()
            
            if hasattr(self, 'status_label'):
                self.status_label.config(text="🟢 System Monitor Active")
            
        except Exception as e:
            error_msg = f"Error updating system info: {str(e)}"
            logging.error(error_msg + f"\n{traceback.format_exc()}")
            if hasattr(self, 'status_label'):
                self.status_label.config(text="🔴 Update Error")
        
        self.root.after(self.update_interval, self.update_system_info)

    def update_processes(self):
        try:
            if not hasattr(self, 'process_tree'):
                return
                
            for item in self.process_tree.get_children():
                self.process_tree.delete(item)
            
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            processes.sort(key=lambda x: x['cpu_percent'] or 0, reverse=True)
            
            for proc in processes[:10]:
                self.process_tree.insert('', 'end', values=(
                    proc['pid'],
                    proc['name'][:30] if proc['name'] else 'N/A',
                    f"{proc['cpu_percent']:.1f}" if proc['cpu_percent'] else '0.0',
                    f"{proc['memory_percent']:.1f}" if proc['memory_percent'] else '0.0'
                ))
                
        except Exception as e:
            logging.error(f"Error updating processes: {e}")

    def view_logs(self):
        try:
            log_window = tk.Toplevel(self.root)
            log_window.title("📋 View Logs")
            log_window.geometry("800x600")
            log_window.resizable(True, True)
            
            log_frame = ttk.Frame(log_window, style='Card.TFrame', padding=10)
            log_frame.pack(fill='both', expand=True)
            
            log_text = tk.Text(log_frame, wrap=tk.NONE, font=('Consolas', 10), height=20)
            log_text.pack(side='left', fill='both', expand=True)
            
            scrollbar_y = ttk.Scrollbar(log_frame, orient='vertical', command=log_text.yview)
            scrollbar_y.pack(side='right', fill='y')
            log_text.config(yscrollcommand=scrollbar_y.set)
            
            scrollbar_x = ttk.Scrollbar(log_frame, orient='horizontal', command=log_text.xview)
            scrollbar_x.pack(side='bottom', fill='x')
            log_text.config(xscrollcommand=scrollbar_x.set)
            
            log_file = "system_monitor.log"
            if os.path.exists(log_file):
                try:
                    with open(log_file, "r", encoding="utf-8") as f:
                        log_content = f.read()
                        log_text.insert(tk.END, log_content)
                        log_text.see(tk.END)
                except Exception as e:
                    log_text.insert(tk.END, f"Error reading log file: {str(e)}")
            else:
                log_text.insert(tk.END, "No log file found.")
            
            log_text.config(state='disabled')
            
            button_frame = ttk.Frame(log_frame)
            button_frame.pack(fill='x', pady=10)
            
            ttk.Button(button_frame, text="Refresh", command=lambda: self.refresh_logs(log_text, log_file), 
                       style='Compact.TButton').pack(side='left', padx=5)
            ttk.Button(button_frame, text="Close", command=log_window.destroy, 
                       style='Compact.TButton').pack(side='right', padx=5)
            
        except Exception as e:
            logging.error(f"Error in view_logs: {str(e)}")

    def refresh_logs(self, log_text, log_file):
        try:
            log_text.config(state='normal')
            log_text.delete(1.0, tk.END)
            if os.path.exists(log_file):
                with open(log_file, "r", encoding="utf-8") as f:
                    log_content = f.read()
                    log_text.insert(tk.END, log_content)
                    log_text.see(tk.END)
            else:
                log_text.insert(tk.END, "No log file found.")
            log_text.config(state='disabled')
        except Exception as e:
            log_text.config(state='normal')
            log_text.insert(tk.END, f"Error refreshing log file: {str(e)}")
            log_text.config(state='disabled')

    def open_settings(self):
        try:
            settings_window = tk.Toplevel(self.root)
            settings_window.title("⚙️ Settings")
            settings_window.geometry("400x300")
            settings_window.resizable(False, False)
            
            settings_frame = ttk.Frame(settings_window, style='Card.TFrame', padding=15)
            settings_frame.pack(fill='both', expand=True)
            
            ttk.Label(settings_frame, text="Update Interval (seconds):", style='Subheader.TLabel').pack(anchor='w', pady=5)
            interval_var = tk.StringVar(value=str(self.update_interval/1000))
            interval_entry = ttk.Entry(settings_frame, textvariable=interval_var, width=10)
            interval_entry.pack(anchor='w', pady=5)
            
            ttk.Label(settings_frame, text="Theme:", style='Subheader.TLabel').pack(anchor='w', pady=5)
            theme_var = tk.StringVar(value=self.style.theme.name)
            theme_combo = ttk.Combobox(settings_frame, textvariable=theme_var, 
                                      values=['cosmo', 'flatly', 'darkly', 'litera'], state='readonly')
            theme_combo.pack(anchor='w', pady=5)
            
            def save_settings():
                try:
                    interval = float(interval_var.get()) * 1000
                    if interval < 500:
                        raise ValueError("Interval must be at least 0.5 seconds")
                    self.update_interval = int(interval)
                    self.update_label.config(text=f"⏱️ Update: {self.update_interval/1000:.1f}s")
                    
                    new_theme = theme_var.get()
                    if new_theme != self.style.theme.name:
                        self.style.theme_use(new_theme)
                    
                    settings_window.destroy()
                    self.status_label.config(text="🟢 Settings saved")
                except ValueError as ve:
                    self.status_label.config(text=f"🔴 {str(ve)}")
                except Exception as e:
                    self.status_label.config(text=f"🔴 Error saving settings: {str(e)}")
            
            button_frame = ttk.Frame(settings_frame)
            button_frame.pack(fill='x', pady=20)
            
            ttk.Button(button_frame, text="Save", command=save_settings, 
                       style='Compact.TButton').pack(side='left', padx=5)
            ttk.Button(button_frame, text="Cancel", command=settings_window.destroy, 
                       style='Compact.TButton').pack(side='right', padx=5)
            
        except Exception as e:
            logging.error(f"Error in open_settings: {str(e)}")

    def refresh_all(self):
        if hasattr(self, 'status_label'):
            self.status_label.config(text="🔄 Refreshing...")
        self.root.after(100, self.update_system_info)

    def export_data(self):
        try:
            filename = f"system_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Metric', 'Value'])
                
                cpu_usage = psutil.cpu_percent(interval=0.1)
                memory = psutil.virtual_memory()
                disk = psutil.disk_usage('C:\\' if platform.system() == 'Windows' else '/')
                net_io = psutil.net_io_counters()
                
                writer.writerow(['CPU Usage (%)', f"{cpu_usage:.1f}"])
                writer.writerow(['Memory Usage (%)', f"{memory.percent:.1f}"])
                writer.writerow(['Memory Total (GB)', f"{memory.total / (1024**3):.1f}"])
                writer.writerow(['Memory Used (GB)', f"{memory.used / (1024**3):.1f}"])
                writer.writerow(['Disk Usage (%)', f"{disk.percent:.1f}"])
                writer.writerow(['Disk Total (GB)', f"{disk.total / (1024**3):.1f}"])
                writer.writerow(['Disk Free (GB)', f"{disk.free / (1024**3):.1f}"])
                writer.writerow(['Network Sent (MB)', f"{net_io.bytes_sent / (1024**2):.1f}"])
                writer.writerow(['Network Received (MB)', f"{net_io.bytes_recv / (1024**2):.1f}"])
                
            self.status_label.config(text=f"🟢 Exported system data to {filename}")
        except Exception as e:
            self.status_label.config(text=f"🔴 Error exporting data: {str(e)}")
            logging.error(f"Error in export_data: {str(e)}")

    def clean_cache(self):
        try:
            cache_files = ['temp_test.txt']
            deleted = 0
            for file in cache_files:
                if os.path.exists(file):
                    os.remove(file)
                    deleted += 1
            self.status_label.config(text=f"🟢 Cleaned {deleted} cache file(s)")
        except Exception as e:
            self.status_label.config(text=f"🔴 Error cleaning cache: {str(e)}")
            logging.error(f"Error in clean_cache: {str(e)}")

    def show_about(self):
        try:
            about_window = tk.Toplevel(self.root)
            about_window.title("❓ About System Monitor")
            about_window.geometry("400x300")
            about_window.resizable(False, False)
            
            about_frame = ttk.Frame(about_window, style='Card.TFrame', padding=15)
            about_frame.pack(fill='both', expand=True)
            
            about_text = """
            🖥️ System Performance Monitor
            
            Version: 1.0.0
            
            A comprehensive system monitoring tool
            with AI and performance testing capabilities.
            
            Built with Python & Tkinter
            Developed by xAI
            """
            
            ttk.Label(about_frame, text=about_text, style='Info.TLabel', 
                     justify='center', anchor='center').pack(expand=True, pady=20)
            
            ttk.Button(about_frame, text="Close", command=about_window.destroy, 
                       style='Compact.TButton').pack(pady=10)
            
        except Exception as e:
            logging.error(f"Error in show_about: {str(e)}")

if __name__ == "__main__":
    import multiprocessing
    multiprocessing.freeze_support()  # เพิ่ม: รองรับ multiprocessing ใน PyInstaller
    root = tk.Tk()
    app = SystemMonitorApp(root)
    root.mainloop()