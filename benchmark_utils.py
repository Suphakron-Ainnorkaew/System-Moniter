import time
import threading
import numpy as np
import logging
from tkinter import messagebox
from datetime import datetime
from system_info_utils import get_hardware_info
from multiprocessing import Pool
import psutil

def benchmark_task(chunk_size):
    """งาน benchmark สำหรับแต่ละ process"""
    np.random.seed(int(time.time() % 10000))
    matrix_size = 1000
    input_data = np.random.rand(matrix_size, matrix_size)
    weights = np.random.rand(matrix_size, matrix_size)
    for _ in range(chunk_size):
        result = np.dot(input_data, weights)
        input_data = result
    return result.sum()

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
        max_cores = psutil.cpu_count(logical=False)  # จำนวน physical cores
        num_cores = max_cores  # ใช้ทุกคอร์
        iterations = 100  # จำนวนรอบต่อ process

        # แบ่งงานให้แต่ละคอร์
        chunk_size = iterations // num_cores
        chunks = [chunk_size] * num_cores
        remaining = iterations % num_cores
        for i in range(remaining):
            chunks[i] += 1

        # รัน benchmark ด้วย multiprocessing
        with Pool(processes=num_cores) as pool:
            while time.time() < end_time and self.is_benchmarking:
                pool.starmap(benchmark_task, [(chunk,) for chunk in chunks])
                # จำลองการใช้หน่วยความจำ
                _ = [np.random.bytes(1024*1024) for _ in range(100)]
                time.sleep(0.1)

        # ดึงข้อมูลฮาร์ดแวร์
        hardware_info = self.hardware_info if hasattr(self, 'hardware_info') else get_hardware_info(self)

        # บันทึกผลลงฐานข้อมูล
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