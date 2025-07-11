import tkinter as tk
from ttkbootstrap import ttk, Style
import test_utils
from system_monitor_db import SystemMonitorDB
import logging
import time
import traceback
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

matplotlib.rcParams['font.family'] = 'Segoe UI'

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')

class TabUtils:
    def __init__(self, master):
        self.master = master
        self.db = SystemMonitorDB()
        self.ai_tests = {
            "Neural Network": {"progress": None, "time": None, "score": None, "row": None},
            "Image Recognition": {"progress": None, "time": None, "score": None, "row": None},
            "Natural Language": {"progress": None, "time": None, "score": None, "row": None},
            "Data Classification": {"progress": None, "time": None, "score": None, "row": None},
            "Clustering": {"progress": None, "time": None, "score": None, "row": None}
        }
        self.pg_tests = {
            "Matrix Multiplication": {"progress": None, "time": None, "score": None, "row": None},
            "File Operations": {"progress": None, "time": None, "score": None, "row": None},
            "String Processing": {"progress": None, "time": None, "score": None, "row": None},
            "Data Sorting": {"progress": None, "time": None, "score": None, "row": None},
            "Image Processing": {"progress": None, "time": None, "score": None, "row": None}
        }
        self.gui_utils = master.gui_utils
        self.test_results = {}
        logging.debug("TabUtils initialized")
        self.setup_styles()

    def setup_styles(self):
        try:
            style = Style(theme='flatly')
            logging.debug("Setting up styles")
            
            style.configure('ModernCard.TFrame',
                            relief='flat',
                            borderwidth=0,
                            background='#ffffff')
            
            style.configure('CompactTitle.TLabel', 
                            font=('Segoe UI', 14, 'bold'),
                            foreground='#2c3e50',
                            background='#ffffff')
            
            style.configure('CompactSubtitle.TLabel', 
                            font=('Segoe UI', 9),
                            foreground='#7f8c8d',
                            background='#ffffff')
            
            style.configure('Compact.TButton',
                            font=('Segoe UI', 9),
                            padding=(12, 6))
            
            style.configure('CompactTest.TLabel',
                            font=('Segoe UI', 9, 'bold'),
                            foreground='#34495e',
                            background='#ffffff')
            
            style.configure('CompactStats.TLabel',
                            font=('Segoe UI', 8),
                            foreground='#7f8c8d',
                            background='#ffffff')
            
        except Exception as e:
            logging.error(f"Error setting up styles: {e}")

    def create_compact_header(self, parent, title, subtitle=None):
        header_frame = ttk.Frame(parent, style='ModernCard.TFrame')
        header_frame.pack(fill='x', pady=(10, 15))
        logging.debug(f"Creating compact header for {title}")
        
        title_label = ttk.Label(header_frame, text=title, style='CompactTitle.TLabel')
        title_label.pack()
        
        if subtitle:
            subtitle_label = ttk.Label(header_frame, text=subtitle, style='CompactSubtitle.TLabel')
            subtitle_label.pack(pady=(2, 8))
        
        separator = ttk.Separator(header_frame, orient='horizontal')
        separator.pack(fill='x', padx=100, pady=(5, 0))
        
        return header_frame

    def create_inline_controls(self, parent, test_type):
        control_frame = ttk.Frame(parent, style='ModernCard.TFrame')
        control_frame.pack(fill='x', pady=(0, 15))
        logging.debug(f"Creating inline controls for {test_type}")
        
        center_frame = ttk.Frame(control_frame, style='ModernCard.TFrame')
        center_frame.pack(anchor='center')
        
        ttk.Label(center_frame, text="Device:", font=('Segoe UI', 9)).pack(side='left', padx=(0, 5))
        
        device_var = getattr(self.master, f'{test_type}_test_device', None)
        if not device_var:
            device_var = tk.StringVar(value="CPU")
            setattr(self.master, f'{test_type}_test_device', device_var)
        
        device_combo = ttk.Combobox(center_frame, textvariable=device_var,
                                    values=["CPU", "GPU"] if test_type == "ai" else ["CPU"],
                                    state='readonly', width=8, font=('Segoe UI', 8))
        device_combo.pack(side='left', padx=(0, 15))
        
        ttk.Label(center_frame, text="Mode:", font=('Segoe UI', 9)).pack(side='left', padx=(0, 5))
        
        mode_var = getattr(self, f'{test_type}_test_mode', None)
        if not mode_var:
            mode_var = tk.StringVar(value="single")
            setattr(self, f'{test_type}_test_mode', mode_var)
        
        mode_values = ["single", "multi", "threaded", "multiprocessing"]
        mode_combo = ttk.Combobox(center_frame, textvariable=mode_var,
                                  values=mode_values,
                                  state='readonly', width=12, font=('Segoe UI', 8))
        mode_combo.pack(side='left', padx=(0, 20))
        
        start_btn = ttk.Button(center_frame, 
                               text=f"Start {test_type.upper()}",
                               command=lambda: self.start_test(test_type),
                               style='Compact.TButton')
        start_btn.pack(side='left', padx=(0, 10))
        
        if test_type == "ai":
            compare_btn = ttk.Button(center_frame,
                                     text="Compare",
                                     command=self.compare_test_modes,
                                     style='Compact.TButton')
            compare_btn.pack(side='left')
        elif test_type == "pg":
            compare_btn = ttk.Button(center_frame,
                                     text="Compare",
                                     command=self.compare_pg_test_modes,
                                     style='Compact.TButton')
            compare_btn.pack(side='left')
    def compare_pg_test_modes(self):
        try:
            logging.debug("Comparing PG test modes")
            output_widget = self.pg_result_text
            output_widget.delete(1.0, tk.END)
            output_widget.insert(tk.END, "Comparing Program test modes...\n")
            output_widget.see(tk.END)

            modes = ["single", "multi", "threaded", "multiprocessing"]
            mode_results = {}

            def run_next_mode(index=0):
                if index >= len(modes):
                    output_widget.insert(tk.END, "\nComparison Summary:\n")
                    for mode in modes:
                        results = self.test_results.get(f"pg_{mode}", {})
                        total_time = sum(data["time"] for data in results.values())
                        avg_score = sum(data["score"] for data in results.values()) / len(results) if results else 0
                        output_widget.insert(tk.END, f"{mode.capitalize()}: Total Time = {total_time:.2f}s, Avg Score = {avg_score:.2f}%\n")
                    output_widget.see(tk.END)
                    self.show_pg_comparison_chart()
                    return

                mode = modes[index]
                output_widget.insert(tk.END, f"\nRunning {mode} mode...\n")
                output_widget.see(tk.END)
                start_time = time.time()
                self.pg_test_mode.set(mode)

                def on_mode_complete():
                    elapsed_time = time.time() - start_time
                    mode_results[mode] = elapsed_time
                    output_widget.insert(tk.END, f"{mode.capitalize()} mode completed in {elapsed_time:.2f}s\n")
                    if elapsed_time > 30:
                        output_widget.insert(tk.END, f"Warning: {mode} mode took too long (>30s)\n")
                    output_widget.see(tk.END)
                    self.show_results_in_new_window("pg", mode)
                    time.sleep(1)
                    run_next_mode(index + 1)

                try:
                    from test_utils import start_tests
                    start_tests(self, "pg", mode, output_widget, callback=on_mode_complete)
                except Exception as e:
                    error_msg = f"Error in {mode} mode: {str(e)}"
                    logging.error(error_msg)
                    output_widget.insert(tk.END, f"{error_msg}\n")
                    output_widget.see(tk.END)
                    run_next_mode(index + 1)

            run_next_mode()

        except Exception as e:
            error_msg = f"Error comparing PG test modes: {str(e)}"
            logging.error(error_msg + f"\n{traceback.format_exc()}")
            output_widget.insert(tk.END, f"Error: {error_msg}\n")
            output_widget.see(tk.END)

    def show_pg_comparison_chart(self):
        try:
            logging.debug("Showing comparison chart for all PG modes")
            def create_chart():
                window = tk.Toplevel(self.master.root)
                window.title("Program Mode Comparison")
                window.geometry("900x600")
                fig = plt.figure(figsize=(12, 6), dpi=100, facecolor='#f8f9fa')
                modes = ["single", "multi", "threaded", "multiprocessing"]
                total_times = []
                avg_scores = []
                for mode in modes:
                    results = self.test_results.get(f"pg_{mode}", {})
                    total_time = sum(data["time"] for data in results.values())
                    avg_score = sum(data["score"] for data in results.values()) / len(results) if results else 0
                    total_times.append(total_time)
                    avg_scores.append(avg_score)
                ax1 = fig.add_subplot(121)
                ax1.bar(modes, total_times, color='#3498db')
                ax1.set_title('Total Time by Mode')
                ax1.set_ylabel('Total Time (s)')
                ax2 = fig.add_subplot(122)
                ax2.bar(modes, avg_scores, color='#e67e22')
                ax2.set_title('Average Score by Mode')
                ax2.set_ylabel('Average Score (%)')
                fig.tight_layout()
                canvas = FigureCanvasTkAgg(fig, master=window)
                canvas.draw()
                canvas.get_tk_widget().pack(fill='both', expand=True)
            self.master.root.after(0, create_chart)
        except Exception as e:
            logging.error(f"Error showing PG comparison chart: {str(e)}\n{traceback.format_exc()}")
        
        return control_frame

    def create_compact_results(self, parent, test_type):
        result_frame = ttk.Frame(parent, style='ModernCard.TFrame')
        result_frame.pack(fill='x', pady=(0, 15))
        logging.debug(f"Creating compact results for {test_type}")
        
        ttk.Label(result_frame, text=f"{test_type.upper()} Results:", 
                  font=('Segoe UI', 10, 'bold'),
                  foreground='#2c3e50',
                  background='#ffffff').pack(pady=(0, 5))
        
        result_text = tk.Text(result_frame, 
                              height=4,
                              font=('Consolas', 8),
                              wrap=tk.WORD,
                              relief='solid',
                              borderwidth=1,
                              bg='#f8f9fa',
                              fg='#2c3e50')
        result_text.pack(fill='x', padx=20)
        
        setattr(self, f'{test_type}_result_text', result_text)
        
        return result_frame

    def create_compact_test_grid(self, parent, test_type):
        grid_frame = ttk.Frame(parent, style='ModernCard.TFrame')
        grid_frame.pack(fill='both', expand=True, pady=(0, 10))
        logging.debug(f"Creating compact test grid for {test_type}")
        
        ttk.Label(grid_frame, text=f"{test_type.upper()} Tests:", 
                  font=('Segoe UI', 10, 'bold'),
                  foreground='#2c3e50',
                  background='#ffffff').pack(pady=(0, 10))
        
        test_configs = {
            "ai": [
                ("Neural Network", "Neural Network"),
                ("Image Recognition", "Image Recognition"),
                ("Natural Language", "Natural Language"),
                ("Data Classification", "Data Classification"),
                ("Clustering", "Clustering")
            ],
            "pg": [
                ("Matrix Multiplication", "Matrix Multiplication"),
                ("File Operations", "File Operations"),
                ("String Processing", "String Processing"),
                ("Data Sorting", "Data Sorting"),
                ("Image Processing", "Image Processing")
            ]
        }
        
        test_dict = getattr(self, f'{test_type}_tests')
        
        tests_container = ttk.Frame(grid_frame, style='ModernCard.TFrame')
        tests_container.pack(padx=30, fill='x')
        
        for i, (display_name, internal_name) in enumerate(test_configs[test_type]):
            test_row = ttk.Frame(tests_container, style='ModernCard.TFrame',
                                 relief='solid', borderwidth=1)
            test_row.pack(fill='x', pady=2, padx=10, ipady=8, ipadx=15)
            
            left_frame = ttk.Frame(test_row, style='ModernCard.TFrame')
            left_frame.pack(side='left', fill='x', expand=True)
            
            test_name_label = ttk.Label(left_frame, text=display_name, 
                                        style='CompactTest.TLabel')
            test_name_label.pack(anchor='w')
            
            right_frame = ttk.Frame(test_row, style='ModernCard.TFrame')
            right_frame.pack(side='right')
            
            progress = ttk.Progressbar(right_frame, 
                                       length=200,
                                       mode='determinate',
                                       style='info.Horizontal.TProgressbar')
            progress.pack(side='left', padx=(0, 10))
            
            stats_frame = ttk.Frame(right_frame, style='ModernCard.TFrame')
            stats_frame.pack(side='left')
            
            time_label = ttk.Label(stats_frame, text="Time: 0.00s", 
                                   style='CompactStats.TLabel')
            time_label.pack()
            
            score_label = ttk.Label(stats_frame, text="Score: 0%", 
                                    style='CompactStats.TLabel')
            score_label.pack()
            
            test_dict[internal_name] = {
                "progress": progress,
                "time": time_label,
                "score": score_label,
                "row": test_row
            }
        
        return grid_frame

    def create_ai_test_tab(self, frame):
        try:
            logging.debug("Creating AI Test tab")
            
            for widget in frame.winfo_children():
                widget.destroy()
            
            main_container = ttk.Frame(frame, style='ModernCard.TFrame')
            main_container.pack(fill='both', expand=True, padx=20, pady=15)
            
            self.create_compact_header(main_container, 
                                       "AI Performance Testing", 
                                       "Evaluate your system's AI capabilities")
            
            self.create_inline_controls(main_container, "ai")
            self.create_compact_results(main_container, "ai")
            self.create_compact_test_grid(main_container, "ai")
            
        except Exception as e:
            error_msg = f"Error creating AI Test tab: {str(e)}"
            logging.error(error_msg + f"\n{traceback.format_exc()}")

    def create_pg_test_tab(self, frame):
        try:
            logging.debug("Creating Program Test tab")
            
            for widget in frame.winfo_children():
                widget.destroy()
            
            main_container = ttk.Frame(frame, style='ModernCard.TFrame')
            main_container.pack(fill='both', expand=True, padx=20, pady=15)
            
            self.create_compact_header(main_container, 
                                       "Program Performance Testing", 
                                       "Benchmark your system's computational performance")
            
            self.create_inline_controls(main_container, "pg")
            self.create_compact_results(main_container, "pg")
            self.create_compact_test_grid(main_container, "pg")
            
        except Exception as e:
            error_msg = f"Error creating Program Test tab: {str(e)}"
            logging.error(error_msg + f"\n{traceback.format_exc()}")

    def start_test(self, test_type):
        try:
            logging.debug(f"Starting {test_type} test")
            mode = getattr(self, f'{test_type}_test_mode', tk.StringVar(value="single")).get()
            output_widget = getattr(self, f'{test_type}_result_text', None)
            if output_widget:
                output_widget.delete(1.0, tk.END)
                output_widget.insert(tk.END, f"Starting {test_type.upper()} test in {mode} mode...\n")
                output_widget.see(tk.END)

            def on_tests_complete():
                logging.debug(f"Test results before chart: {self.test_results.get(f'{test_type}_{mode}', {})}")
                completed_tests = len(self.test_results.get(f'{test_type}_{mode}', {}))
                if completed_tests > 0:
                    self.show_results_in_new_window(test_type, mode)
                else:
                    logging.warning(f"No tests completed for {test_type} in {mode}")
                    if output_widget:
                        output_widget.insert(tk.END, "\nWarning: No tests completed\n")
                        output_widget.see(tk.END)

            from test_utils import start_tests
            start_tests(self, test_type, mode, output_widget, callback=on_tests_complete)

        except Exception as e:
            logging.error(f"Error starting {test_type} test: {str(e)}")
            if output_widget:
                output_widget.insert(tk.END, f"Error: {str(e)}\n")
                output_widget.see(tk.END)

    def compare_test_modes(self):
        try:
            logging.debug("Comparing test modes")
            output_widget = self.ai_result_text
            output_widget.delete(1.0, tk.END)
            output_widget.insert(tk.END, "Comparing AI test modes...\n")
            output_widget.see(tk.END)

            modes = ["single", "multi", "threaded", "multiprocessing"]
            mode_results = {}

            def run_next_mode(index=0):
                if index >= len(modes):
                    output_widget.insert(tk.END, "\nComparison Summary:\n")
                    for mode in modes:
                        results = self.test_results.get(f"ai_{mode}", {})
                        total_time = sum(data["time"] for data in results.values())
                        avg_score = sum(data["score"] for data in results.values()) / len(results) if results else 0
                        output_widget.insert(tk.END, f"{mode.capitalize()}: Total Time = {total_time:.2f}s, Avg Score = {avg_score:.2f}%\n")
                    output_widget.see(tk.END)
                    self.show_comparison_chart()
                    return

                mode = modes[index]
                output_widget.insert(tk.END, f"\nRunning {mode} mode...\n")
                output_widget.see(tk.END)

                start_time = time.time()
                self.ai_test_mode.set(mode)

                def on_mode_complete():
                    elapsed_time = time.time() - start_time
                    mode_results[mode] = elapsed_time
                    output_widget.insert(tk.END, f"{mode.capitalize()} mode completed in {elapsed_time:.2f}s\n")
                    if elapsed_time > 30:
                        output_widget.insert(tk.END, f"Warning: {mode} mode took too long (>30s)\n")
                    output_widget.see(tk.END)
                    self.show_results_in_new_window("ai", mode)
                    time.sleep(1)
                    run_next_mode(index + 1)

                try:
                    from test_utils import start_tests
                    start_tests(self, "ai", mode, output_widget, callback=on_mode_complete)
                except Exception as e:
                    error_msg = f"Error in {mode} mode: {str(e)}"
                    logging.error(error_msg)
                    output_widget.insert(tk.END, f"{error_msg}\n")
                    output_widget.see(tk.END)
                    run_next_mode(index + 1)

            run_next_mode()

        except Exception as e:
            error_msg = f"Error comparing test modes: {str(e)}"
            logging.error(error_msg + f"\n{traceback.format_exc()}")
            output_widget.insert(tk.END, f"Error: {error_msg}\n")
            output_widget.see(tk.END)

    def show_comparison_chart(self):
        try:
            logging.debug("Showing comparison chart for all modes")
            def create_chart():
                window = tk.Toplevel(self.master.root)
                window.title("AI Mode Comparison")
                window.geometry("900x600")
                fig = plt.figure(figsize=(12, 6), dpi=100, facecolor='#f8f9fa')
                canvas = FigureCanvasTkAgg(fig, master=window)
                canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)

                ax = fig.add_subplot(111)
                test_configs = ["Neural Network", "Image Recognition", "Natural Language", "Data Classification", "Clustering"]
                modes = ["single", "multi", "threaded", "multiprocessing"]
                colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']

                for idx, mode in enumerate(modes):
                    results = self.test_results.get(f"ai_{mode}", {})
                    scores = [results.get(name, {"score": 0})["score"] for name in test_configs]
                    ax.plot(test_configs, scores, label=mode.capitalize(), color=colors[idx], marker='o', linewidth=2)

                ax.set_xlabel('Tests', fontsize=10)
                ax.set_ylabel('Score (%)', fontsize=10)
                ax.set_title('AI Mode Comparison (Score)', fontsize=14, fontweight='bold')
                ax.legend()
                ax.grid(True, linestyle='--', alpha=0.3)
                ax.set_facecolor('#f8f9fa')
                fig.tight_layout()

                canvas.draw()

                close_btn = ttk.Button(window, text="Close", command=window.destroy, style='Compact.TButton')
                close_btn.pack(pady=10)

            # เพิ่ม: รันใน main thread
            self.master.root.after(0, create_chart)
        except Exception as e:
            logging.error(f"Error showing comparison chart: {str(e)}")
            output_widget = self.ai_result_text
            if output_widget:
                output_widget.insert(tk.END, f"\nError displaying comparison chart: {str(e)}\n")
                output_widget.see(tk.END)

    def update_test_progress(self, test_type, test_name, elapsed_time, score):
        try:
            test_dict = getattr(self, f'{test_type}_tests')
            logging.debug(f"Updating progress for {test_type}/{test_name}")
            
            if test_name in test_dict and test_dict[test_name]["progress"]:
                widgets = test_dict[test_name]
                widgets["progress"]["value"] = 100 if elapsed_time > 0 else 0
                widgets["time"].config(text=f"Time: {elapsed_time:.2f}s")
                widgets["score"].config(text=f"Score: {score:.2f}%")

                self.test_results.setdefault(f"{test_type}_{getattr(self, f'{test_type}_test_mode').get()}", {})[test_name] = {
                    "time": elapsed_time,
                    "score": score
                }
                logging.debug(f"Stored result for {test_type}/{test_name}: time={elapsed_time:.2f}s, score={score:.2f}%")
                
                if score >= 80:
                    widgets["progress"].config(style='success.Horizontal.TProgressbar')
                elif score >= 60:
                    widgets["progress"].config(style='warning.Horizontal.TProgressbar')
                else:
                    widgets["progress"].config(style='danger.Horizontal.TProgressbar')
                    
        except Exception as e:
            logging.error(f"Error updating test progress: {str(e)}")

    def show_results_in_new_window(self, test_type, mode=None):
        try:
            mode = mode or getattr(self, f'{test_type}_test_mode').get()
            logging.debug(f"Opening new window to display {test_type} results for {mode}")
            window = tk.Toplevel(self.master.root)
            window.title(f"{test_type.upper()} Results ({mode.capitalize()})")
            window.geometry("900x600")
            window.resizable(True, False)
            
            fig = plt.figure(figsize=(12, 6), dpi=100, facecolor='#f8f9fa')
            canvas = FigureCanvasTkAgg(fig, master=window)
            canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)
            
            self.display_test_results_chart(test_type, mode, fig, canvas)
            
            close_btn = ttk.Button(window, 
                                   text="Close",
                                   command=window.destroy,
                                   style='Compact.TButton')
            close_btn.pack(pady=10)
            
        except Exception as e:
            logging.error(f"Error showing results in new window: {str(e)}")
            output_widget = getattr(self, f'{test_type}_result_text', None)
            if output_widget:
                output_widget.insert(tk.END, f"\nError displaying results window: {str(e)}\n")
                output_widget.see(tk.END)

    def show_empty_chart(self, test_type, mode, fig, canvas):
        try:
            logging.debug(f"Showing empty chart for {test_type} {mode}")
            fig.clear()
            fig.patch.set_facecolor('#f8f9fa')
            ax = fig.add_subplot(111)
            ax.set_facecolor('#ffffff')
            
            ax.text(0.5, 0.6, f'Ready to test {test_type.capitalize()} Performance ({mode})', 
                    horizontalalignment='center',
                    verticalalignment='center',
                    transform=ax.transAxes,
                    fontsize=12,
                    fontweight='bold',
                    color='#2c3e50')
            
            ax.text(0.5, 0.4, 'Click Start button to begin testing',
                    horizontalalignment='center',
                    verticalalignment='center',
                    transform=ax.transAxes,
                    fontsize=10,
                    color='#666666')
            
            ax.set_xticks([])
            ax.set_yticks([])
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['bottom'].set_visible(False)
            ax.spines['left'].set_visible(False)
            
            fig.suptitle(f"{test_type.upper()} Performance Testing ({mode})", fontsize=14, fontweight='bold')
            fig.subplots_adjust(left=0.1, right=0.9, top=0.85, bottom=0.15)
            
            canvas.draw()
            
        except Exception as e:
            logging.error(f"Error showing empty chart: {str(e)}")

    def display_test_results_chart(self, test_type, mode, fig, canvas):
        try:
            logging.debug(f"Displaying results chart for {test_type} {mode}")
            def create_chart():
                results = self.test_results.get(f"{test_type}_{mode}", {})
                logging.debug(f"Test results: {results}")

                if not results:
                    output_widget = getattr(self, f'{test_type}_result_text', None)
                    if output_widget:
                        output_widget.insert(tk.END, f"\nNo test results available for {mode} mode\n")
                        output_widget.see(tk.END)
                    self.show_empty_chart(test_type, mode, fig, canvas)
                    return

                test_configs = {
                    "ai": ["Neural Network", "Image Recognition", "Natural Language", "Data Classification", "Clustering"],
                    "pg": ["Matrix Multiplication", "File Operations", "String Processing", "Data Sorting", "Image Processing"]
                }
                test_order = test_configs.get(test_type, [])

                test_names = [name for name in test_order if name in results]
                times = [results[name]["time"] for name in test_names]
                scores = [results[name]["score"] for name in test_names]

                if not test_names:
                    logging.debug("No valid test names found for chart")
                    output_widget = getattr(self, f'{test_type}_result_text', None)
                    if output_widget:
                        output_widget.insert(tk.END, f"\nNo valid test results for {mode} mode\n")
                        output_widget.see(tk.END)
                    self.show_empty_chart(test_type, mode, fig, canvas)
                    logging.warning(f"No valid test results for {test_type} {mode}")
                    return

                short_names = [name.replace(" ", "\n") for name in test_names]

                fig.clear()
                fig.patch.set_facecolor('#f8f9fa')

                ax1 = fig.add_subplot(121)
                ax2 = fig.add_subplot(122)

                time_colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#34495E']
                score_colors = ['#3498DB', '#9B59B6', '#E74C3C', '#F1C40F', '#2ECC71']
                time_colors = time_colors[:len(test_names)]
                score_colors = score_colors[:len(test_names)]

                bars1 = ax1.bar(range(len(test_names)), times, color=time_colors, alpha=0.8, edgecolor='white', linewidth=1)
                ax1.set_title('Execution Time', fontsize=12, fontweight='bold', pad=15)
                ax1.set_ylabel('Time (seconds)', fontsize=10)
                ax1.set_xticks(range(len(test_names)))
                ax1.set_xticklabels(short_names, fontsize=10, ha='center')
                ax1.grid(True, axis='y', linestyle='--', alpha=0.3)
                ax1.set_facecolor('#f8f9fa')
                for bar, time_val in zip(bars1, times):
                    height = bar.get_height()
                    ax1.text(bar.get_x() + bar.get_width()/2., height + max(times)*0.02, 
                            f'{time_val:.2f}s', ha='center', va='bottom', fontsize=8)

                bars2 = ax2.bar(range(len(test_names)), scores, color=score_colors, alpha=0.8, edgecolor='white', linewidth=1)
                ax2.set_title('Performance Score', fontsize=12, fontweight='bold', pad=15)
                ax2.set_ylabel('Score (%)', fontsize=10)
                ax2.set_xticks(range(len(test_names)))
                ax2.set_xticklabels(short_names, fontsize=10, ha='center')
                ax2.set_ylim(0, 110)
                ax2.grid(True, axis='y', linestyle='--', alpha=0.3)
                ax2.set_facecolor('#f8f9fa')
                for bar, score in zip(bars2, scores):
                    height = bar.get_height()
                    ax2.text(bar.get_x() + bar.get_width()/2., height + 2, 
                            f'{score:.1f}%', ha='center', va='bottom', fontsize=8)

                avg_score = sum(scores) / len(scores) if scores else 0
                ax2.axhline(y=avg_score, color='red', linestyle='--', alpha=0.7, linewidth=1.5)
                ax2.text(len(test_names)-0.5, avg_score + 5, f'Avg: {avg_score:.1f}%', 
                        color='red', fontsize=9, ha='right')

                fig.suptitle(f'{test_type.upper()} Performance Results ({mode.capitalize()})', fontsize=14, fontweight='bold', y=0.95)
                fig.subplots_adjust(left=0.08, right=0.95, top=0.85, bottom=0.15, wspace=0.3)

                total_time = sum(times) if times else 0
                avg_time = total_time / len(times) if times else 0
                max_score = max(scores) if scores else 0
                min_score = min(scores) if scores else 0

                stats_text = (f"Summary Statistics:\n"
                            f"Total Time: {total_time:.2f}s\n"
                            f"Average Time: {avg_time:.2f}s\n"
                            f"Best Score: {max_score:.1f}%\n"
                            f"Lowest Score: {min_score:.1f}%\n"
                            f"Tests Completed: {len(test_names)}/{len(test_order)}")
                fig.text(0.02, 0.02, stats_text, fontsize=9, 
                        bbox=dict(boxstyle="round", facecolor="white", alpha=0.9, edgecolor="gray"),
                        verticalalignment='bottom')

                canvas.draw()

                output_widget = getattr(self, f'{test_type}_result_text', None)
                if output_widget:
                    output_widget.insert(tk.END, f"\nResults displayed in new window for {mode} mode\n")
                    output_widget.insert(tk.END, f"Completed {len(test_names)} tests\n")
                    output_widget.insert(tk.END, f"Total time: {total_time:.2f}s\n")
                    output_widget.insert(tk.END, f"Average score: {avg_score:.2f}%\n")
                    if len(test_names) < len(test_order):
                        output_widget.insert(tk.END, f"Warning: Only {len(test_names)}/{len(test_order)} tests completed\n")
                    output_widget.see(tk.END)

            # เพิ่ม: รันใน main thread
            self.master.root.after(0, create_chart)
        except Exception as e:
            logging.error(f"Error displaying test results chart: {str(e)}")
            output_widget = getattr(self, f'{test_type}_result_text', None)
            if output_widget:
                output_widget.insert(tk.END, f"\nError displaying results chart: {str(e)}\n")
                output_widget.see(tk.END)