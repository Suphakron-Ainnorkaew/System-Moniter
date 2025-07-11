import requests
import logging

API_URL = "http://localhost:5000/submit"  # เปลี่ยนเป็น URL ที่ deploy จริง

class SystemMonitorDB:
    def __init__(self):
        logging.debug("SystemMonitorDB now uses API, no local DB init.")

    def insert_benchmark_log(self, test_type, total_time, avg_score, device, mode, cpu_brand=None, cpu_info=None, scores_dict=None):
        # Get GPU info (prefer NVIDIA if available)
        gpu_brand = None
        gpu_model = None
        try:
            import pythoncom
            pythoncom.CoInitialize()
            import wmi
            c = wmi.WMI()
            gpu_list = c.Win32_VideoController()
            nvidia_gpu = None
            for gpu in gpu_list:
                name = gpu.Name
                if "NVIDIA" in name.upper():
                    nvidia_gpu = gpu
                    break
            if nvidia_gpu:
                gpu_model = nvidia_gpu.Name
                gpu_brand = "NVIDIA"
            elif gpu_list:
                gpu_model = gpu_list[0].Name
                if "INTEL" in gpu_model.upper():
                    gpu_brand = "Intel"
                elif "AMD" in gpu_model.upper():
                    gpu_brand = "AMD"
                else:
                    gpu_brand = "Unknown"
        except Exception as gpu_e:
            logging.warning(f"Cannot get GPU info: {gpu_e}")

        # Get RAM info
        ram_gb = None
        try:
            import psutil
            ram_gb = int(psutil.virtual_memory().total / (1024**3))
        except Exception as ram_e:
            logging.warning(f"Cannot get RAM info: {ram_e}")

        # Prepare data for API
        data = {
            "model_name": device,
            "cpu_brand": cpu_brand,
            "cpu_model": cpu_info,
            "gpu_brand": gpu_brand,
            "gpu_model": gpu_model,
            "ram_gb": ram_gb,
            "test_details": {
                "test_type": test_type,
                "mode": mode,
                "total_time": total_time,
                "avg_score": avg_score,
                "scores": scores_dict
            }
        }
        try:
            response = requests.post(API_URL, json=data, timeout=10)
            response.raise_for_status()
            result = response.json()
            if result.get('status') == 'ok':
                logging.info("Benchmark data sent to API successfully.")
                return True
            else:
                logging.error(f"API error: {result.get('message')}")
                return False
        except Exception as e:
            logging.error(f"Error sending data to API: {e}")
            return False