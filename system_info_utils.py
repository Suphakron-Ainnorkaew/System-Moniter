import psutil
import time
import subprocess
import wmi

def update_system_info(self):
    if not hasattr(self, 'hardware_info'):
        self.hardware_info = get_hardware_info(self)

    while self.monitoring:  # ใช้ self.monitoring เพื่อหยุด loop เมื่อปิดโปรแกรม
        try:
            cpu_percent = psutil.cpu_percent()
            self.cpu_percent.configure(text=f"{cpu_percent}%")
            self.cpu_progress['value'] = cpu_percent
            if cpu_percent > self.benchmark_data['cpu_max']:
                self.benchmark_data['cpu_max'] = cpu_percent

            gpu_percent = self.get_gpu_usage()
            self.gpu_percent.configure(text=f"{gpu_percent}%")
            self.gpu_progress['value'] = gpu_percent
            if gpu_percent > self.benchmark_data['gpu_max']:
                self.benchmark_data['gpu_max'] = gpu_percent

            ram = psutil.virtual_memory()
            ram_percent = ram.percent
            ram_total = ram.total / (1024**3)
            self.ram_percent.configure(text=f"{ram_percent}%")
            self.ram_progress['value'] = ram_percent
            self.total_ram.configure(text=f"Total: {ram_total:.1f} GB")
            if ram_percent > self.benchmark_data['memory_max']:
                self.benchmark_data['memory_max'] = ram_percent

            disk = psutil.disk_usage('/')
            storage_percent = disk.percent
            storage_total = disk.total / (1024**3)
            self.storage_percent.configure(text=f"{storage_percent}%")
            self.storage_progress['value'] = storage_percent
            self.total_storage.configure(text=f"Total: {storage_total:.1f} GB")

            if int(time.time()) % 5 == 0:
                self.db.save_system_log(cpu_percent, gpu_percent, ram_percent, storage_percent)

            time.sleep(1)

        except Exception as e:
            print(f"Error updating system info: {e}")
            time.sleep(1)

def get_gpu_usage(self):
    try:
        output = subprocess.check_output(['nvidia-smi', '--query-gpu=utilization.gpu', '--format=csv'])
        gpu_usage = int(output.decode('utf-8').split('\n')[1].strip().split('%')[0])
        return gpu_usage
    except Exception as e:
        print(f"Error getting GPU usage: {str(e)}")
        return 0

def get_gpu_memory(self):
    try:
        output = subprocess.check_output(['nvidia-smi', '--query-gpu=memory.used', '--format=csv'])
        gpu_memory = int(output.decode('utf-8').split('\n')[1].strip().split('MiB')[0])
        return gpu_memory
    except Exception as e:
        print(f"Error getting GPU memory: {str(e)}")
        return 0

def get_gpu_total_memory(self):
    try:
        output = subprocess.check_output(['nvidia-smi', '--query-gpu=memory.total', '--format=csv'])
        gpu_total_memory = int(output.decode('utf-8').split('\n')[1].strip().split('MiB')[0])
        return gpu_total_memory
    except Exception as e:
        print(f"Error getting GPU total memory: {str(e)}")
        return 0

def get_gpu_temperature(self):
    try:
        output = subprocess.check_output(['nvidia-smi', '--query-gpu=temperature.gpu', '--format=csv'])
        gpu_temperature = int(output.decode('utf-8').split('\n')[1].strip().split('C')[0])
        return gpu_temperature
    except Exception as e:
        print(f"Error getting GPU temperature: {str(e)}")
        return 0

def check_ai_capability(self):
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    total_ram = ram.total / (1024**3)
    used_ram = (ram.total - ram.available) / (1024**3)
    ram_percent = ram.percent

    total_storage = disk.total / (1024**3)
    used_storage = disk.used / (1024**3)
    storage_percent = disk.percent

    info_text = "🖥️ ข้อมูลการใช้งานระบบ:\n\n"
    info_text += f"📊 RAM Usage:\n"
    info_text += f"RAM ทั้งหมด: {total_ram:.1f} GB\n"
    info_text += f"RAM ที่ใช้: {used_ram:.1f} GB\n"
    info_text += f"เปอร์เซ็นต์การใช้ RAM: {ram_percent}%\n\n"
    info_text += f"💾 Storage Usage:\n"
    info_text += f"พื้นที่ทั้งหมด: {total_storage:.1f} GB\n"
    info_text += f"พื้นที่ที่ใช้: {used_storage:.1f} GB\n"
    info_text += f"เปอร์เซ็นต์การใช้พื้นที่: {storage_percent}%\n\n"

    gpus = self.get_gpu_count()
    has_gpu = len(gpus) > 0
    sufficient_ram = total_ram >= 8

    info_text += "🤖 ความสามารถในการรัน AI:\n"
    if has_gpu and sufficient_ram:
        gpu_name = self.get_gpu_name()
        info_text += f"✅ ระบบสามารถรัน AI ได้\nGPU: {gpu_name}\nRAM: {total_ram:.1f}GB"
        self.status_label.configure(text="System Status: Excellent", foreground="#4CAF50")
    elif has_gpu:
        info_text += "⚠️ ระบบมี GPU แต่ RAM ไม่เพียงพอ\nแนะนำให้มี RAM อย่างน้อย 8GB"
        self.status_label.configure(text="System Status: Fair", foreground="#FF9800")
    elif sufficient_ram:
        info_text += "⚠️ ระบบมี RAM เพียงพอแต่ไม่พบ GPU\nอาจรัน AI ได้ช้าหรือมีข้อจำกัด"
        self.status_label.configure(text="System Status: Fair", foreground="#FF9800")
    else:
        info_text += "❌ ระบบไม่เหมาะสมสำหรับการรัน AI\nต้องการ GPU และ RAM อย่างน้อย 8GB"
        self.status_label.configure(text="System Status: Poor", foreground="#F44336")

    self.info_text.delete(1.0, tk.END)
    self.info_text.insert(1.0, info_text)

def get_gpu_count(self):
    try:
        output = subprocess.check_output(['nvidia-smi', '--query-gpu=count', '--format=csv'])
        gpu_count = int(output.decode('utf-8').split('\n')[1].strip())
        return [1] * gpu_count
    except Exception as e:
        print(f"Error getting GPU count: {str(e)}")
        return []

def get_gpu_name(self):
    try:
        output = subprocess.check_output(['nvidia-smi', '--query-gpu=name', '--format=csv'])
        gpu_name = output.decode('utf-8').split('\n')[1].strip()
        return gpu_name
    except Exception as e:
        print(f"Error getting GPU name: {str(e)}")
        return ""

def get_hardware_info(self):
    hardware_info = {}
    try:
        computer = wmi.WMI()
        cpu_info = computer.Win32_Processor()[0]
        hardware_info['cpu_brand'] = f"{cpu_info.Manufacturer} {cpu_info.Name.strip()}"

        board = computer.Win32_BaseBoard()[0]
        hardware_info['mainboard'] = f"{board.Manufacturer} {board.Product}"

        memory_info = computer.Win32_PhysicalMemory()
        if memory_info:
            ram = memory_info[0]
            hardware_info['ram_brand'] = f"{ram.Manufacturer} {ram.Speed}MHz {int(float(ram.Capacity) / 1024 / 1024 / 1024)}GB"
        else:
            hardware_info['ram_brand'] = "Unknown"

        disk_info = computer.Win32_DiskDrive()
        if disk_info:
            hardware_info['storage_brand'] = disk_info[0].Model
        else:
            hardware_info['storage_brand'] = "Unknown"
    except Exception as e:
        print(f"Error getting hardware info with WMI: {e}")
        hardware_info['cpu_brand'] = "Unknown"
        hardware_info['mainboard'] = "Unknown"
        hardware_info['ram_brand'] = "Unknown"
        hardware_info['storage_brand'] = "Unknown"

    try:
        nvidia_smi = subprocess.check_output(["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"]).decode().strip()
        hardware_info['gpu_brand'] = nvidia_smi
    except:
        try:
            gpu = computer.Win32_VideoController()[0]
            hardware_info['gpu_brand'] = gpu.Name
        except:
            hardware_info['gpu_brand'] = "Unknown"

    return hardware_info