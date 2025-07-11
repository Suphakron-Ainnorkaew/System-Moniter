import tkinter as tk
from ttkbootstrap import ttk
import psutil
import wmi
import logging
import traceback

class GUIUtils:
    def __init__(self, master):
        self.master = master
        self.cpu_label = None
        self.memory_label = None
        self.disk_label = None

    def create_system_monitor_tab(self, frame):
        try:
            logging.debug("Creating system monitor tab")
            stat_frame = ttk.LabelFrame(frame, text="System Stats", padding=10)
            stat_frame.pack(fill='x', padx=10, pady=10)

            self.cpu_label = ttk.Label(stat_frame, text="CPU Usage: 0%")
            self.cpu_label.pack(anchor='w', pady=5)
            
            self.memory_label = ttk.Label(stat_frame, text="Memory Usage: 0%")
            self.memory_label.pack(anchor='w', pady=5)
            
            self.disk_label = ttk.Label(stat_frame, text="Disk Usage: 0%")
            self.disk_label.pack(anchor='w', pady=5)

        except Exception as e:
            error_msg = f"Error creating system monitor tab: {str(e)}"
            logging.error(error_msg + f"\n{traceback.format_exc()}")
            print(error_msg + f"\n{traceback.format_exc()}")

    def create_sections(self, parent, title, items):
        try:
            logging.debug(f"Creating section: {title}")
            section_frame = ttk.LabelFrame(parent, text=title, padding=10)
            section_frame.pack(fill='x', padx=5, pady=5)
            for item in items:
                label = ttk.Label(section_frame, text=item)
                label.pack(anchor='w', pady=2)
            return section_frame
        except Exception as e:
            error_msg = f"Error creating section {title}: {str(e)}"
            logging.error(error_msg + f"\n{traceback.format_exc()}")
            print(error_msg + f"\n{traceback.format_exc()}")