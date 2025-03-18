import sqlite3
from datetime import datetime

class SystemMonitorDB:
    def __init__(self, db_name="system_monitor.db"):
        self.db_name = db_name
        self.create_tables()

    def create_tables(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # ตาราง system_logs
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                cpu_percent REAL,
                gpu_percent REAL,
                ram_percent REAL,
                storage_percent REAL
            )
        ''')

        # ตาราง benchmarks
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS benchmarks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                cpu_max REAL,
                gpu_max REAL,
                memory_max REAL,
                duration INTEGER,
                notes TEXT,
                cpu_brand TEXT,
                gpu_brand TEXT,
                ram_brand TEXT,
                storage_brand TEXT,
                mainboard TEXT
            )
        ''')

        # ตารางtest_results
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS test_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                test_type TEXT,
                device TEXT,
                test_name TEXT,
                score REAL,
                elapsed_time REAL
            )
        ''')

        conn.commit()
        conn.close()

    def save_system_log(self, cpu_percent, gpu_percent, ram_percent, storage_percent):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        timestamp = datetime.now().isoformat()
        cursor.execute('''
            INSERT INTO system_logs (timestamp, cpu_percent, gpu_percent, ram_percent, storage_percent)
            VALUES (?, ?, ?, ?, ?)
        ''', (timestamp, cpu_percent, gpu_percent, ram_percent, storage_percent))
        conn.commit()
        conn.close()

    def save_benchmark(self, cpu_max, gpu_max, memory_max, duration, notes, 
                       cpu_brand, gpu_brand, ram_brand, storage_brand, mainboard):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        timestamp = datetime.now().isoformat()
        cursor.execute('''
            INSERT INTO benchmarks (timestamp, cpu_max, gpu_max, memory_max, duration, notes, 
                                   cpu_brand, gpu_brand, ram_brand, storage_brand, mainboard)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (timestamp, cpu_max, gpu_max, memory_max, duration, notes, 
              cpu_brand, gpu_brand, ram_brand, storage_brand, mainboard))
        conn.commit()
        conn.close()

    def save_test_result(self, test_type, device, test_name, score, elapsed_time):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        timestamp = datetime.now().isoformat()
        cursor.execute('''
            INSERT INTO test_results (timestamp, test_type, device, test_name, score, elapsed_time)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (timestamp, test_type, device, test_name, score, elapsed_time))
        conn.commit()
        conn.close()

    def get_recent_benchmarks(self, limit=20):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM benchmarks ORDER BY timestamp DESC LIMIT ?', (limit,))
        results = cursor.fetchall()
        conn.close()
        return results

    def get_test_results(self, limit=20):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM test_results ORDER BY timestamp DESC LIMIT ?', (limit,))
        results = cursor.fetchall()
        conn.close()
        return results