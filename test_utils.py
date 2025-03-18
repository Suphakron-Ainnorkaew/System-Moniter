import time
import threading
import numpy as np
import os
import tkinter as tk
from system_monitor_db import SystemMonitorDB  # Import เพื่อใช้ DB

def start_pg_tests(self):
    print("Starting Program Tests...")
    self.pg_result_text.delete(1.0, tk.END)
    for test_data in self.pg_tests.values():
        test_data["progress"]["value"] = 0
        test_data["time"].configure(text="Time: 0.00s")
        test_data["score"].configure(text="Score: 0%")

    def run_tests():
        print(f"Running tests in thread: {threading.current_thread().name}")
        device = self.pg_test_device.get()
        results = []
        total_score = 0
        db = SystemMonitorDB()

        for test_name, test_data in self.pg_tests.items():
            print(f"Starting {test_name} on {device}")
            start_time = time.time()

            if test_name == "Matrix Multiplication":
                for i in range(100):
                    np.random.rand(500, 500).dot(np.random.rand(500, 500))
                    self.master.after(0, lambda: test_data["progress"].configure(value=(i + 1) * 1.0))
                    time.sleep(0.01)
            elif test_name == "File Operations":
                for i in range(100):
                    with open("test.txt", "w") as f:
                        f.write("test" * 1000)
                    self.master.after(0, lambda: test_data["progress"].configure(value=(i + 1) * 1.0))
                    time.sleep(0.01)
            elif test_name == "String Processing":
                for i in range(100):
                    _ = "test" * 1000 + str(i)
                    self.master.after(0, lambda: test_data["progress"].configure(value=(i + 1) * 1.0))
                    time.sleep(0.01)
            elif test_name == "Data Sorting":
                for i in range(100):
                    data = np.random.rand(1000)
                    data.sort()
                    self.master.after(0, lambda: test_data["progress"].configure(value=(i + 1) * 1.0))
                    time.sleep(0.01)
            elif test_name == "Image Processing":
                for i in range(100):
                    _ = np.random.rand(100, 100) * 255
                    self.master.after(0, lambda: test_data["progress"].configure(value=(i + 1) * 1.0))
                    time.sleep(0.01)

            end_time = time.time()
            elapsed = end_time - start_time
            score = min(100, int(1000 / elapsed))
            total_score += score

            # บันทึกผลลงฐานข้อมูล
            db.save_test_result("Program", device, test_name, score, elapsed)

            self.master.after(0, lambda: test_data["time"].configure(text=f"Time: {elapsed:.2f}s"))
            self.master.after(0, lambda: test_data["score"].configure(text=f"Score: {score}%"))
            results.append(f"{test_name} ({device}): {elapsed:.2f}s, Score: {score}%")

        avg_score = total_score / len(self.pg_tests)
        analysis = f"\nProgram Tests on {device.upper()}:\n" + "\n".join(results) + "\nCompleted.\n"
        analysis += f"\nคะแนนเฉลี่ย: {avg_score:.1f}%\n"
        if avg_score >= 80:
            analysis += "✅ เครื่องนี้เหมาะมากสำหรับการเขียนโปรแกรมทั่วไป!\nประสิทธิภาพสูง ทำงานได้รวดเร็วและลื่นไหล"
        elif avg_score >= 50:
            analysis += "⚠️ เครื่องนี้ใช้เขียนโปรแกรมทั่วไปได้ แต่ประสิทธิภาพปานกลาง\nอาจช้าลงในงานที่ซับซ้อน แนะนำอัปเกรด CPU/GPU หรือ RAM"
        else:
            analysis += "❌ เครื่องนี้ไม่เหมาะกับการเขียนโปรแกรม\nประสิทธิภาพต่ำเกินไป แนะนำอัปเกรดเครื่องใหม่"

        # แสดงผลการทดสอบล่าสุดจากฐานข้อมูล
        recent_results = db.get_test_results(limit=5)
        analysis += "\n\nผลการทดสอบล่าสุด:\n"
        for result in recent_results:
            analysis += f"{result[1]} - {result[2]} on {result[3]} - {result[4]}: Score {result[5]}%, Time {result[6]:.2f}s\n"

        self.master.after(0, lambda: self.pg_result_text.insert(tk.END, analysis))
        print("Program Tests completed")

    test_thread = threading.Thread(target=run_tests)
    test_thread.daemon = True
    test_thread.start()
    print("Test thread started")

def start_ai_tests(self):
    print("Starting AI Tests...")
    self.ai_result_text.delete(1.0, tk.END)
    for test_data in self.ai_tests.values():
        test_data["progress"]["value"] = 0
        test_data["time"].configure(text="Time: 0.00s")
        test_data["score"].configure(text="Score: 0%")

    def run_tests():
        print(f"Running tests in thread: {threading.current_thread().name}")
        device = self.ai_test_device.get()
        results = []
        total_score = 0
        db = SystemMonitorDB()

        for test_name, test_data in self.ai_tests.items():
            print(f"Starting {test_name} on {device}")
            start_time = time.time()

            if test_name == "Neural Network":
                for i in range(100):
                    np.random.rand(1000, 1000)
                    self.master.after(0, lambda: test_data["progress"].configure(value=(i + 1) * 1.0))
                    time.sleep(0.02)
            elif test_name == "Image Recognition":
                for i in range(100):
                    _ = np.random.rand(224, 224, 3)
                    self.master.after(0, lambda: test_data["progress"].configure(value=(i + 1) * 1.0))
                    time.sleep(0.02)
            elif test_name == "Natural Language":
                for i in range(100):
                    _ = ["word"] * 1000
                    self.master.after(0, lambda: test_data["progress"].configure(value=(i + 1) * 1.0))
                    time.sleep(0.02)
            elif test_name == "Data Classification":
                for i in range(100):
                    data = np.random.rand(1000)
                    _ = data > 0.5
                    self.master.after(0, lambda: test_data["progress"].configure(value=(i + 1) * 1.0))
                    time.sleep(0.02)
            elif test_name == "Clustering":
                for i in range(100):
                    _ = np.random.rand(1000, 2)
                    self.master.after(0, lambda: test_data["progress"].configure(value=(i + 1) * 1.0))
                    time.sleep(0.02)

            end_time = time.time()
            elapsed = end_time - start_time
            score = min(100, int(500 / elapsed))
            total_score += score

            # บันทึกผลลงฐานข้อมูล
            db.save_test_result("AI", device, test_name, score, elapsed)

            self.master.after(0, lambda: test_data["time"].configure(text=f"Time: {elapsed:.2f}s"))
            self.master.after(0, lambda: test_data["score"].configure(text=f"Score: {score}%"))
            results.append(f"{test_name} ({device}): {elapsed:.2f}s, Score: {score}%")

        avg_score = total_score / len(self.ai_tests)
        analysis = f"\nAI Tests on {device.upper()}:\n" + "\n".join(results) + "\nCompleted.\n"
        analysis += f"\nคะแนนเฉลี่ย: {avg_score:.1f}%\n"
        if avg_score >= 80:
            analysis += "✅ เครื่องนี้เหมาะมากสำหรับการพัฒนา AI!\nประสิทธิภาพสูง รองรับงาน AI ได้ดีเยี่ยม"
        elif avg_score >= 50:
            analysis += "⚠️ เครื่องนี้ใช้พัฒนา AI ได้ แต่ประสิทธิภาพปานกลาง\nอาจช้าในงานหนัก แนะนำใช้ GPU ที่ดีขึ้นหรือเพิ่ม RAM"
        else:
            analysis += "❌ เครื่องนี้ไม่เหมาะกับการพัฒนา AI\nประสิทธิภาพต่ำเกินไป แนะนำอัปเกรด GPU และ RAM"

        # แสดงผลการทดสอบล่าสุดจากฐานข้อมูล
        recent_results = db.get_test_results(limit=5)
        analysis += "\n\nผลการทดสอบล่าสุด:\n"
        for result in recent_results:
            analysis += f"{result[1]} - {result[2]} on {result[3]} - {result[4]}: Score {result[5]}%, Time {result[6]:.2f}s\n"

        self.master.after(0, lambda: self.ai_result_text.insert(tk.END, analysis))
        print("AI Tests completed")

    test_thread = threading.Thread(target=run_tests)
    test_thread.daemon = True
    test_thread.start()
    print("Test thread started")

def update_test_progress(self, test_name, progress_value):
    if test_name in self.pg_tests:
        self.master.after(0, lambda: self.pg_tests[test_name]["progress"].configure(value=progress_value))
    elif test_name in self.ai_tests:
        self.master.after(0, lambda: self.ai_tests[test_name]["progress"].configure(value=progress_value))