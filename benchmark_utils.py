import time
import threading
import numpy as np
import logging
from tkinter import messagebox
from datetime import datetime
from system_info_utils import get_hardware_info

def start_benchmark(self):
    if self.is_benchmarking:
        messagebox.showwarning("Warning", "Benchmark กำลังทำงานอยู่")
        return

    try:
        duration = int(self.stress_duration.get())
        if duration <= 0:
            raise ValueError("Duration must be positive")
    except ValueError:
        messagebox.showerror("Error", "กรุณาใส่จำนวนวินาทีที่ถูกต้อง")
        return

    self.is_benchmarking = True
    self.benchmark_data = {
        'cpu_max': 0,
        'gpu_max': 0,
        'memory_max': 0,
        'start_time': time.time()
    }
    self.start_benchmark_btn.configure(state='disabled')
    self.benchmark_status.configure(text="กำลังทำ Benchmark...")

    threading.Thread(target=self.run_stress_test, args=(duration,), daemon=True).start()

def run_stress_test(self, duration):
    try:
        logging.info(f"Starting benchmark for {duration} seconds")
        end_time = time.time() + duration

        while time.time() < end_time and self.is_benchmarking:
            np.random.rand(1000, 1000).dot(np.random.rand(1000, 1000))
            _ = [np.random.bytes(1024*1024) for _ in range(100)]
            time.sleep(0.1)

        # ดึงข้อมูลฮาร์ดแวร์ (ใช้จาก self.hardware_info ที่มีอยู่แล้ว)
        hardware_info = self.hardware_info if hasattr(self, 'hardware_info') else get_hardware_info(self)

        # บันทึกผลลงฐานข้อมูลพร้อมข้อมูลฮาร์ดแวร์
        self.db.save_benchmark(
            self.benchmark_data['cpu_max'],
            self.benchmark_data['gpu_max'],
            self.benchmark_data['memory_max'],
            duration,
            f"Benchmark completed at {datetime.now()}",
            hardware_info['cpu_brand'],
            hardware_info['gpu_brand'],
            hardware_info['ram_brand'],
            hardware_info['storage_brand'],
            hardware_info['mainboard']
        )

        self.is_benchmarking = False
        self.start_benchmark_btn.configure(state='normal')
        self.benchmark_status.configure(
            text=f"Benchmark เสร็จสิ้น - CPU Max: {self.benchmark_data['cpu_max']:.1f}% "
                 f"GPU Max: {self.benchmark_data['gpu_max']:.1f}% "
                 f"Memory Max: {self.benchmark_data['memory_max']:.1f}%"
        )

    except Exception as e:
        logging.error(f"Benchmark error: {str(e)}")
        self.is_benchmarking = False
        self.start_benchmark_btn.configure(state='normal')
        self.benchmark_status.configure(text=f"Benchmark ผิดพลาด: {str(e)}")