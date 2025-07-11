import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk

def view_logs(self):
    logs_window = tk.Toplevel(self.master)
    logs_window.title("System Logs")
    logs_window.geometry("600x400")

    text_widget = tk.Text(logs_window, wrap=tk.WORD, font=("Consolas", 10))
    scrollbar = ttk.Scrollbar(logs_window, orient="vertical", command=text_widget.yview)
    text_widget.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    text_widget.pack(fill=tk.BOTH, expand=True)

    try:
        with open('system_monitor.log', 'r', encoding='utf-8') as f:
            logs = f.read()
            text_widget.insert(tk.END, logs)
    except Exception as e:
        text_widget.insert(tk.END, f"Error reading logs: {str(e)}")

    text_widget.configure(state='disabled')

def view_benchmark_history(self):
    history_window = tk.Toplevel(self.master)
    history_window.title("Benchmark History")
    history_window.geometry("800x400")

    columns = ('Timestamp', 'CPU Max', 'GPU Max', 'Memory Max', 'Duration', 'Notes', 'CPU', 'GPU', 'RAM', 'Storage', 'Mainboard')
    tree = ttk.Treeview(history_window, columns=columns, show='headings', style='primary.Treeview')
    
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, stretch=True)

    scrollbar = ttk.Scrollbar(history_window, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(fill=tk.BOTH, expand=True)

    try:
        benchmarks = self.db.get_recent_benchmarks(limit=20)
        for benchmark in benchmarks:
            tree.insert('', tk.END, values=benchmark[1:])
    except Exception as e:
        tk.Label(history_window, text=f"Error loading benchmarks: {str(e)}", foreground="red").pack()

    history_window.update()