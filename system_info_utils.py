import psutil
import time
import platform
import wmi
import subprocess
import threading

def update_system_info(app):
    while app.monitoring:
        try:
            cpu_usage = psutil.cpu_percent(interval=0.1)
            app.cpu_percent.config(text=f"{cpu_usage:.1f}%")
            app.cpu_progress["value"] = cpu_usage

            memory = psutil.virtual_memory()
            app.ram_percent.config(text=f"{memory.percent:.1f}%")
            app.ram_progress["value"] = memory.percent
            app.total_ram.config(text=f"Total: {memory.total / (1024**3):.2f} GB")

            disk = psutil.disk_usage('/')
            app.storage_percent.config(text=f"{disk.percent:.1f}%")
            app.storage_progress["value"] = disk.percent
            app.total_storage.config(text=f"Total: {disk.total / (1024**3):.2f} GB")

            try:
                nvidia_smi = subprocess.check_output(["nvidia-smi", "--query-gpu=utilization.gpu,memory.used,memory.total", "--format=csv,noheader"], text=True)
                gpu_load, gpu_mem_used, gpu_mem_total = nvidia_smi.strip().split(", ")
                gpu_load = float(gpu_load.replace(" %", ""))
                gpu_mem_used = float(gpu_mem_used.replace(" MiB", ""))
                gpu_mem_total = float(gpu_mem_total.replace(" MiB", ""))
                app.gpu_percent.config(text=f"{gpu_load:.1f}%")
                app.gpu_progress["value"] = gpu_load
                app.gpu_memory.config(text=f"Memory: {gpu_mem_used:.0f}/{gpu_mem_total:.0f} MB")
            except:
                app.gpu_percent.config(text="N/A")
                app.gpu_memory.config(text="GPU: Not detected")
                app.gpu_progress["value"] = 0

            try:
                w = wmi.WMI(namespace="root\\wmi")
                temp = w.MSAcpi_ThermalZoneTemperature()[0].CurrentTemperature / 10.0 - 273.15
                app.cpu_temp.config(text=f"Temperature: {temp:.1f}°C")
            except:
                app.cpu_temp.config(text="Temperature: N/A")

            system_info = f"""
System: {platform.system()} {platform.release()}
Processor: {platform.processor()}
Cores: {psutil.cpu_count(logical=False)} (Logical: {psutil.cpu_count()})
Total RAM: {memory.total / (1024**3):.2f} GB
Total Storage: {disk.total / (1024**3):.2f} GB
"""
            app.info_text.delete(1.0, 'end')
            app.info_text.insert(1.0, system_info.strip())

            try:
                if hasattr(app.db, 'log_system_data'):
                    app.db.log_system_data(cpu_usage, gpu_load if 'gpu_load' in locals() else 0, memory.percent, disk.percent)
                else:
                    print("Warning: log_system_data not found in SystemMonitorDB")
            except Exception as e:
                print(f"Error logging system data: {e}")

        except Exception as e:
            print(f"Error updating system info: {e}")

        time.sleep(1)

def check_ai_capability(app):
    while app.monitoring:
        try:
            gpu_available = False
            try:
                nvidia_smi = subprocess.check_output(["nvidia-smi"], text=True)
                gpu_available = True
            except:
                pass

            cpu_cores = psutil.cpu_count(logical=False)
            total_ram = psutil.virtual_memory().total / (1024**3)

            if gpu_available and cpu_cores >= 8 and total_ram >= 16:
                app.benchmark_status.config(text="System Status: Excellent", foreground="#4CAF50")
            elif cpu_cores >= 4 and total_ram >= 8:
                app.benchmark_status.config(text="System Status: Good", foreground="#FFC107")
            else:
                app.benchmark_status.config(text="System Status: Limited", foreground="#F44336")

            app.hardware_info["gpu_available"] = gpu_available
            app.hardware_info["cpu_cores"] = cpu_cores
            app.hardware_info["total_ram"] = total_ram

        except Exception as e:
            print(f"Error checking AI capability: {e}")
            app.benchmark_status.config(text="System Status: Error", foreground="#F44336")

        time.sleep(10)