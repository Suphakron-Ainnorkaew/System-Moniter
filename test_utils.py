import logging
import platform
import wmi
import time
import random
import string
import threading
import psutil
import traceback
import tkinter as tk
import matplotlib
import tkinter.messagebox as msgbox
import multiprocessing
from multiprocessing import Pool, Manager
from sklearn.datasets import make_classification
from sklearn.neural_network import MLPClassifier
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import numpy as np
import os
import sys
import json

BASELINE_FILE = "baseline.json"

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def monitor_resources(output_widget, stop_event, root):
    try:
        while not stop_event.is_set():
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            root.after(0, lambda: output_widget.insert(tk.END, f"CPU: {cpu_percent:.1f}% | Memory: {memory_percent:.1f}%\n"))
            root.after(0, lambda: output_widget.see(tk.END))
            time.sleep(1)
    except Exception as e:
        error_msg = f"Error in monitor_resources: {str(e)}\n{traceback.format_exc()}"
        logging.error(error_msg)
        root.after(0, lambda msg=f"Error: {str(e)}\n": output_widget.insert(tk.END, msg))
        root.after(0, lambda: output_widget.see(tk.END))

def calculate_time_factor(elapsed_time, max_time=5.0):
    return min(max(0.5, 1 - (elapsed_time / max_time) * 0.5), 1.0)

def simulate_neural_network(mode="single"):
    logging.debug(f"Starting {simulate_neural_network.__name__} in {mode} mode")
    try:
        start_time = time.time()
        X, y = make_classification(n_samples=1000, n_features=20, n_informative=10, random_state=42)
        clf = MLPClassifier(hidden_layer_sizes=(50,), max_iter=200, random_state=42)
        clf.fit(X, y)
        elapsed_time = time.time() - start_time
        score = min(100 / (elapsed_time + 0.1) * 5, 100)
        score *= calculate_time_factor(elapsed_time)
        logging.debug(f"Finished {simulate_neural_network.__name__} in {elapsed_time:.2f}s, score={score:.2f}")
        return elapsed_time, score
    except Exception as e:
        logging.error(f"Error in {simulate_neural_network.__name__}: {str(e)}\n{traceback.format_exc()}")
        raise

def simulate_image_recognition(mode="single"):
    logging.debug(f"Starting {simulate_image_recognition.__name__} in {mode} mode")
    try:
        start_time = time.time()
        img_size = 16
        num_classes = 5
        num_samples = 500
        X = np.random.rand(num_samples, img_size, img_size, 3)
        y = np.random.randint(0, num_classes, num_samples)
        X_flat = X.reshape(num_samples, -1)
        clf = MLPClassifier(hidden_layer_sizes=(50,), max_iter=200, random_state=42)
        clf.fit(X_flat, y)
        elapsed_time = time.time() - start_time
        score = min(100 / (elapsed_time + 0.1) * 5, 100)
        score *= calculate_time_factor(elapsed_time)
        logging.debug(f"Finished {simulate_image_recognition.__name__} in {elapsed_time:.2f}s, score={score:.2f}")
        return elapsed_time, score
    except Exception as e:
        logging.error(f"Error in {simulate_image_recognition.__name__}: {str(e)}\n{traceback.format_exc()}")
        raise

def simulate_natural_language(mode="single"):
    logging.debug(f"Starting {simulate_natural_language.__name__} in {mode} mode")
    try:
        start_time = time.time()
        num_samples = 1000
        vocab_size = 5000
        X = np.random.rand(num_samples, vocab_size)
        y = np.random.randint(0, 2, num_samples)
        clf = MLPClassifier(hidden_layer_sizes=(50,), max_iter=200, random_state=42)
        clf.fit(X, y)
        elapsed_time = time.time() - start_time
        score = min(100 / (elapsed_time + 0.1) * 5, 100)
        score *= calculate_time_factor(elapsed_time)
        logging.debug(f"Finished {simulate_natural_language.__name__} in {elapsed_time:.2f}s, score={score:.2f}")
        return elapsed_time, score
    except Exception as e:
        logging.error(f"Error in {simulate_natural_language.__name__}: {str(e)}\n{traceback.format_exc()}")
        raise

def simulate_data_classification(mode="single"):
    logging.debug(f"Starting {simulate_data_classification.__name__} in {mode} mode")
    try:
        start_time = time.time()
        X, y = make_classification(
            n_samples=500,
            n_features=20,
            n_informative=10,
            n_redundant=5,
            n_clusters_per_class=2,
            n_classes=4,
            class_sep=0.8,
            random_state=42
        )
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        clf = MLPClassifier(hidden_layer_sizes=(50,), max_iter=200, random_state=42)
        clf.fit(X_scaled, y)
        y_pred = clf.predict(X_scaled)
        accuracy = accuracy_score(y, y_pred)
        elapsed_time = time.time() - start_time
        score = min(accuracy * 100, 100)
        score *= calculate_time_factor(elapsed_time)
        logging.debug(f"Finished {simulate_data_classification.__name__} in {elapsed_time:.2f}s, score={score:.2f}")
        return elapsed_time, score
    except Exception as e:
        logging.error(f"Error in {simulate_data_classification.__name__}: {str(e)}\n{traceback.format_exc()}")
        raise

def simulate_clustering(mode="single"):
    logging.debug(f"Starting {simulate_clustering.__name__} in {mode} mode")
    try:
        start_time = time.time()
        X, _ = make_classification(n_samples=5000, n_features=50, n_informative=25, random_state=42)
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        kmeans = KMeans(n_clusters=10, n_init=10, random_state=42)
        kmeans.fit(X_scaled)
        elapsed_time = time.time() - start_time
        score = min(100 / (elapsed_time + 0.1) * 5, 100)
        score *= calculate_time_factor(elapsed_time)
        logging.debug(f"Finished {simulate_clustering.__name__} in {elapsed_time:.2f}s, score={score:.2f}")
        return elapsed_time, score
    except Exception as e:
        logging.error(f"Error in {simulate_clustering.__name__}: {str(e)}\n{traceback.format_exc()}")
        raise

def simulate_matrix_multiplication(mode="single"):
    logging.debug(f"Starting {simulate_matrix_multiplication.__name__} in {mode} mode")
    try:
        start_time = time.time()
        size = 500
        matrix_a = np.random.rand(size, size)
        matrix_b = np.random.rand(size, size)
        result = np.dot(matrix_a, matrix_b)
        elapsed_time = time.time() - start_time
        score = min(100 / (elapsed_time + 0.1) * 5, 100)
        score *= calculate_time_factor(elapsed_time)
        logging.debug(f"Finished {simulate_matrix_multiplication.__name__} in {elapsed_time:.2f}s, score={score:.2f}")
        return elapsed_time, score
    except Exception as e:
        logging.error(f"Error in {simulate_matrix_multiplication.__name__}: {str(e)}\n{traceback.format_exc()}")
        raise

def simulate_file_operations(mode="single"):
    logging.debug(f"Starting {simulate_file_operations.__name__} in {mode} mode")
    try:
        start_time = time.time()
        temp_file = resource_path("temp_test.txt")
        with open(temp_file, "w", encoding='utf-8') as f:
            for _ in range(5000):
                f.write("".join(random.choices(string.ascii_letters, k=100)) + "\n")
        with open(temp_file, "r", encoding='utf-8') as f:
            data = f.read()
        os.remove(temp_file)
        elapsed_time = time.time() - start_time
        base_score = min(100 / (elapsed_time + 0.1) * 5, 100)
        score = base_score * calculate_time_factor(elapsed_time, max_time=3.0)
        logging.debug(f"Finished {simulate_file_operations.__name__} in {elapsed_time:.2f}s, score={score:.2f}")
        return elapsed_time, score
    except Exception as e:
        logging.error(f"Error in {simulate_file_operations.__name__}: {str(e)}\n{traceback.format_exc()}")
        raise

def simulate_string_processing(mode="single"):
    logging.debug(f"Starting {simulate_string_processing.__name__} in {mode} mode")
    try:
        start_time = time.time()
        text = "".join(random.choices(string.ascii_letters, k=1000000))
        processed_text = text.upper().replace('A', 'Z').replace('E', 'Y')
        word_count = len(processed_text.split())
        elapsed_time = time.time() - start_time
        score = min(100 / (elapsed_time + 0.1) * 5, 100)
        score *= calculate_time_factor(elapsed_time)
        logging.debug(f"Finished {simulate_string_processing.__name__} in {elapsed_time:.2f}s, score={score:.2f}")
        return elapsed_time, score
    except Exception as e:
        logging.error(f"Error in {simulate_string_processing.__name__}: {str(e)}\n{traceback.format_exc()}")
        raise

def simulate_data_sorting(mode="single"):
    logging.debug(f"Starting {simulate_data_sorting.__name__} in {mode} mode")
    try:
        start_time = time.time()
        data = [random.randint(0, 1000000) for _ in range(100000)]
        sorted_data = sorted(data)
        elapsed_time = time.time() - start_time
        score = min(100 / (elapsed_time + 0.1) * 5, 100)
        score *= calculate_time_factor(elapsed_time)
        logging.debug(f"Finished {simulate_data_sorting.__name__} in {elapsed_time:.2f}s, score={score:.2f}")
        return elapsed_time, score
    except Exception as e:
        logging.error(f"Error in {simulate_data_sorting.__name__}: {str(e)}\n{traceback.format_exc()}")
        raise

def simulate_image_processing(mode="single"):
    logging.debug(f"Starting {simulate_image_processing.__name__} in {mode} mode")
    try:
        start_time = time.time()
        img_size = 256
        image = np.random.rand(img_size, img_size, 3)
        from scipy.ndimage import gaussian_filter
        blurred = gaussian_filter(image, sigma=2)
        elapsed_time = time.time() - start_time
        score = min(100 / (elapsed_time + 0.1) * 5, 100)
        score *= calculate_time_factor(elapsed_time)
        logging.debug(f"Finished {simulate_image_processing.__name__} in {elapsed_time:.2f}s, score={score:.2f}")
        return elapsed_time, score
    except Exception as e:
        logging.error(f"Error in {simulate_image_processing.__name__}: {str(e)}\n{traceback.format_exc()}")
        raise


# For multiprocessing (3 args, no GUI, no shared objects)
def run_test(args):
    test_func, test_name, mode = args
    logging.debug(f"Running test: {test_name} in {mode} mode")
    try:
        if multiprocessing.current_process().name != "MainProcess":
            matplotlib.use('Agg')
        elapsed_time, score = test_func(mode=mode)
        if elapsed_time > 30:
            raise TimeoutError(f"Test {test_name} took too long: {elapsed_time:.2f}s")
        return (test_name, elapsed_time, score)
    except Exception as e:
        error_msg = f"Error in {test_name}: {str(e)}"
        logging.error(f"{error_msg}\n{traceback.format_exc()}")
        return (test_name, 0, 0, error_msg)

# For single, threaded, multi (5 args, with shared objects)
def run_test_local(args):
    test_func, test_name, results, result_list, mode = args
    logging.debug(f"Running test: {test_name} in {mode} mode (local)")
    try:
        if multiprocessing.current_process().name != "MainProcess":
            matplotlib.use('Agg')
        elapsed_time, score = test_func(mode=mode)
        if elapsed_time > 30:
            raise TimeoutError(f"Test {test_name} took too long: {elapsed_time:.2f}s")
        results[test_name] = {"time": elapsed_time, "score": score}
        result_list.append((test_name, elapsed_time, score))
        logging.debug(f"Completed test: {test_name} in {elapsed_time:.2f}s, score={score:.2f}")
        return elapsed_time, score
    except Exception as e:
        error_msg = f"Error in {test_name}: {str(e)}"
        logging.error(f"{error_msg}\n{traceback.format_exc()}")
        print(f"{error_msg}\n{traceback.format_exc()}")
        result_list.append((test_name, 0, 0, error_msg))
        return 0, 0

def get_baseline_file(device_type, test_type):
    # AI test: ใช้ cpubaseline.json/gpubaseline.json, PG test: ใช้ cpuplbaseline.json/gpuplbaseline.json
    if test_type == "ai":
        return "gpubaseline.json" if device_type == "gpu" else "cpubaseline.json"
    elif test_type == "pg":
        return "gpuplbaseline.json" if device_type == "gpu" else "cpuplbaseline.json"
    else:
        return "baseline.json"

def load_baseline(device_type="cpu", mode="single", test_type="ai"):
    baseline_file = get_baseline_file(device_type, test_type)
    if os.path.exists(baseline_file):
        with open(baseline_file, "r", encoding="utf-8") as f:
            all_baseline = json.load(f)
            return all_baseline.get(mode, {})
    return {}

def save_baseline(baseline, device_type="cpu", mode="single", test_type="ai"):
    baseline_file = get_baseline_file(device_type, test_type)
    all_baseline = {}
    if os.path.exists(baseline_file):
        with open(baseline_file, "r", encoding="utf-8") as f:
            all_baseline = json.load(f)
    all_baseline[mode] = baseline
    print(f"DEBUG: save_baseline to {baseline_file} for mode={mode}")
    print(f"DEBUG: baseline keys now: {list(all_baseline.keys())}")
    with open(baseline_file, "w", encoding="utf-8") as f:
        json.dump(all_baseline, f, indent=2)

def calculate_baseline_score(test_name, elapsed_time, baseline):
    base_time = baseline.get(test_name)
    if base_time is None or elapsed_time <= 0:
        return 100.0  # Default score if no baseline or invalid time
    return (base_time / elapsed_time) * 100

def start_tests(tab_utils, test_type, mode, output_widget, callback=None, device_type="cpu"):
    logging.debug(f"Starting {test_type} tests in {mode} mode")
    try:
        root = tab_utils.master.root
        root.after(0, lambda: output_widget.delete(1.0, tk.END))
        root.after(0, lambda: output_widget.insert(tk.END, f"Starting {test_type.upper()} tests in {mode} mode...\n"))
        root.after(0, lambda: output_widget.see(tk.END))

        tests = tab_utils.ai_tests if test_type == "ai" else tab_utils.pg_tests
        for test_name, test_data in tests.items():
            root.after(0, lambda td=test_data: td["progress"].configure(value=0))
            root.after(0, lambda td=test_data: td["time"].configure(text="Time: 0.00s"))
            root.after(0, lambda td=test_data: td["score"].configure(text="Score: 0"))

        stop_event = threading.Event()
        monitor_thread = threading.Thread(target=monitor_resources, args=(output_widget, stop_event, root), daemon=True)
        monitor_thread.start()

        baseline = load_baseline(device_type, mode, test_type)

        def run_all_tests():
            baseline_updated = False  # ป้องกัน UnboundLocalError
            try:
                results = {}
                result_list = []
                processed_tests = set()

                test_functions = {
                    "ai": {
                        "Neural Network": simulate_neural_network,
                        "Image Recognition": simulate_image_recognition,
                        "Natural Language": simulate_natural_language,
                        "Data Classification": simulate_data_classification,
                        "Clustering": simulate_clustering
                    },
                    "pg": {
                        "Matrix Multiplication": simulate_matrix_multiplication,
                        "File Operations": simulate_file_operations,
                        "String Processing": simulate_string_processing,
                        "Data Sorting": simulate_data_sorting,
                        "Image Processing": simulate_image_processing,
                    }
                }

                cpu_count = psutil.cpu_count(logical=True)
                if mode in ["single", "threaded"]:
                    proc = psutil.Process()
                    proc.cpu_affinity([0])

                if mode == "single":
                    for test_name in test_functions[test_type].keys():
                        if test_name in tests:
                            test_func = test_functions[test_type][test_name]
                            elapsed_time, _ = run_test_local((test_func, test_name, results, result_list, mode))
                            # Baseline logic
                            if test_name not in baseline or baseline[test_name] <= 0:
                                baseline[test_name] = elapsed_time
                                baseline_updated = True
                                score = 100.0
                                root.after(0, lambda msg=f"[BASELINE] {test_name}: Time = {elapsed_time:.2f}s set as baseline.\n": output_widget.insert(tk.END, msg))
                            else:
                                score = calculate_baseline_score(test_name, elapsed_time, baseline)
                            test_data = tests[test_name]
                            root.after(0, lambda td=test_data: td["progress"].configure(value=100))
                            root.after(0, lambda msg=f"{test_name}: Time = {elapsed_time:.2f}s, Score = {score:.2f}\n": output_widget.insert(tk.END, msg))
                            root.after(0, lambda td=test_data, t=elapsed_time: td["time"].configure(text=f"Time: {t:.2f}s"))
                            root.after(0, lambda td=test_data, s=score: td["score"].configure(text=f"Score: {s:.2f}"))
                            root.after(0, lambda: tab_utils.update_test_progress(test_type, test_name, elapsed_time, score))
                            processed_tests.add(test_name)
                            results[test_name] = {"time": elapsed_time, "score": score}

                elif mode == "multi" or mode == "threaded":
                    threads = []
                    for test_name in test_functions[test_type].keys():
                        if test_name in tests:
                            test_func = test_functions[test_type][test_name]
                            thread = threading.Thread(
                                target=run_test_local,
                                args=((test_func, test_name, results, result_list, mode),),
                                daemon=True
                            )
                            threads.append(thread)
                            thread.start()

                    for thread in threads:
                        thread.join(timeout=60)

                    for result in result_list:
                        if len(result) == 4:
                            test_name, elapsed_time, _, error = result
                            if test_name not in processed_tests and test_name in tests:
                                test_data = tests[test_name]
                                if test_name not in baseline or baseline[test_name] <= 0:
                                    baseline[test_name] = elapsed_time
                                    baseline_updated = True
                                    score = 100.0
                                    root.after(0, lambda msg=f"[BASELINE] {test_name}: Time = {elapsed_time:.2f}s set as baseline.\n": output_widget.insert(tk.END, msg))
                                else:
                                    score = calculate_baseline_score(test_name, elapsed_time, baseline)
                                root.after(0, lambda msg=f"{test_name}: {error}\n": output_widget.insert(tk.END, msg))
                                root.after(0, lambda td=test_data: td["progress"].configure(value=0))
                                root.after(0, lambda td=test_data, t=elapsed_time: td["time"].configure(text=f"Time: {t:.2f}s"))
                                root.after(0, lambda td=test_data, s=score: td["score"].configure(text=f"Score: {s:.2f}"))
                                root.after(0, lambda: tab_utils.update_test_progress(test_type, test_name, elapsed_time, score))
                                processed_tests.add(test_name)
                                results[test_name] = {"time": elapsed_time, "score": score}
                        else:
                            test_name, elapsed_time, _ = result
                            if test_name not in processed_tests and test_name in tests:
                                test_data = tests[test_name]
                                if test_name not in baseline or baseline[test_name] <= 0:
                                    baseline[test_name] = elapsed_time
                                    baseline_updated = True
                                    score = 100.0
                                    root.after(0, lambda msg=f"[BASELINE] {test_name}: Time = {elapsed_time:.2f}s set as baseline.\n": output_widget.insert(tk.END, msg))
                                else:
                                    score = calculate_baseline_score(test_name, elapsed_time, baseline)
                                root.after(0, lambda td=test_data: td["progress"].configure(value=100))
                                root.after(0, lambda msg=f"{test_name}: Time = {elapsed_time:.2f}s, Score = {score:.2f}\n": output_widget.insert(tk.END, msg))
                                root.after(0, lambda td=test_data, t=elapsed_time: td["time"].configure(text=f"Time: {t:.2f}s"))
                                root.after(0, lambda td=test_data, s=score: td["score"].configure(text=f"Score: {s:.2f}"))
                                root.after(0, lambda: tab_utils.update_test_progress(test_type, test_name, elapsed_time, score))
                                processed_tests.add(test_name)
                                results[test_name] = {"time": elapsed_time, "score": score}
                        root.after(0, lambda: output_widget.see(tk.END))

                elif mode == "multiprocessing":
                    try:
                        multiprocessing.set_start_method('spawn', force=True)
                    except RuntimeError:
                        pass  # already set
                    try:
                        with Pool(processes=min(len(tests), max(1, cpu_count // 2))) as pool:
                            args = [
                                (test_functions[test_type][test_name], test_name, mode)
                                for test_name in test_functions[test_type].keys() if test_name in tests
                            ]
                            mp_results = pool.map(run_test, args)
                    except Exception as e:
                        error_msg = f"Multiprocessing error: {str(e)}\n{traceback.format_exc()}"
                        logging.error(error_msg)
                        root.after(0, lambda msg=f"Multiprocessing error: {str(e)}\n": output_widget.insert(tk.END, msg))
                        root.after(0, lambda: output_widget.see(tk.END))
                        mp_results = []

                    if not mp_results:
                        root.after(0, lambda: output_widget.insert(tk.END, "No results returned from multiprocessing.\n"))
                        root.after(0, lambda: output_widget.see(tk.END))

                    for result in mp_results:
                        if len(result) == 4:
                            test_name, elapsed_time, _, error = result
                            if test_name not in processed_tests and test_name in tests:
                                test_data = tests[test_name]
                                if test_name not in baseline or baseline[test_name] <= 0:
                                    baseline[test_name] = elapsed_time
                                    baseline_updated = True
                                    score = 100.0
                                    root.after(0, lambda msg=f"[BASELINE] {test_name}: Time = {elapsed_time:.2f}s set as baseline.\n": output_widget.insert(tk.END, msg))
                                else:
                                    score = calculate_baseline_score(test_name, elapsed_time, baseline)
                                root.after(0, lambda msg=f"{test_name}: {error}\n": output_widget.insert(tk.END, msg))
                                root.after(0, lambda td=test_data: td["progress"].configure(value=0))
                                root.after(0, lambda td=test_data, t=elapsed_time: td["time"].configure(text=f"Time: {t:.2f}s"))
                                root.after(0, lambda td=test_data, s=score: td["score"].configure(text=f"Score: {s:.2f}"))
                                root.after(0, lambda: tab_utils.update_test_progress(test_type, test_name, elapsed_time, score))
                                processed_tests.add(test_name)
                                results[test_name] = {"time": elapsed_time, "score": score}
                        else:
                            test_name, elapsed_time, _ = result
                            if test_name not in processed_tests and test_name in tests:
                                test_data = tests[test_name]
                                if test_name not in baseline or baseline[test_name] <= 0:
                                    baseline[test_name] = elapsed_time
                                    baseline_updated = True
                                    score = 100.0
                                    root.after(0, lambda msg=f"[BASELINE] {test_name}: Time = {elapsed_time:.2f}s set as baseline.\n": output_widget.insert(tk.END, msg))
                                else:
                                    score = calculate_baseline_score(test_name, elapsed_time, baseline)
                                root.after(0, lambda td=test_data: td["progress"].configure(value=100))
                                root.after(0, lambda msg=f"{test_name}: Time = {elapsed_time:.2f}s, Score = {score:.2f}\n": output_widget.insert(tk.END, msg))
                                root.after(0, lambda td=test_data, t=elapsed_time: td["time"].configure(text=f"Time: {t:.2f}s"))
                                root.after(0, lambda td=test_data, s=score: td["score"].configure(text=f"Score: {s:.2f}"))
                                root.after(0, lambda: tab_utils.update_test_progress(test_type, test_name, elapsed_time, score))
                                processed_tests.add(test_name)
                                results[test_name] = {"time": elapsed_time, "score": score}
                        root.after(0, lambda: output_widget.see(tk.END))

                else:
                    raise ValueError(f"Unsupported mode: {mode}")

                missing_tests = set(test_functions[test_type].keys()) & set(tests.keys()) - processed_tests
                if missing_tests:
                    logging.warning(f"Missing test results for: {missing_tests}")
                    for test_name in missing_tests:
                        test_data = tests[test_name]
                        root.after(0, lambda td=test_data: td["progress"].configure(value=0))
                        root.after(0, lambda td=test_data: td["time"].configure(text="Time: 0.00s"))
                        root.after(0, lambda td=test_data: td["score"].configure(text="Score: 0"))
                        root.after(0, lambda: tab_utils.update_test_progress(test_type, test_name, 0, 0))
                        results[test_name] = {"time": 0, "score": 0}

                stop_event.set()
                if monitor_thread.is_alive():
                    monitor_thread.join(timeout=2)

                valid_results = {k: v for k, v in results.items() if isinstance(v, dict) and v.get("time", 0) > 0}
                total_time = sum(data["time"] for data in valid_results.values())
                avg_score = sum(data["score"] for data in valid_results.values()) / len(valid_results) if valid_results else 0

                logging.debug(f"Results: {results}, Total Time: {total_time:.2f}s, Avg Score: {avg_score:.2f}")
                tab_utils.test_results[f"{test_type}_{mode}"] = dict(valid_results)

                root.after(0, lambda: output_widget.insert(tk.END, f"\n{test_type.upper()} tests ({mode}) completed!\n"))
                root.after(0, lambda: output_widget.insert(tk.END, f"Total Time: {total_time:.2f}s\n"))
                root.after(0, lambda: output_widget.insert(tk.END, f"Average Score: {avg_score:.2f}\n"))
                root.after(0, lambda: output_widget.see(tk.END))

                # --- Pop-up Alert: แจ้งเตือนความเหมาะสม ---
                # ใช้ค่าเฉลี่ย ratio ของทุก test ในโหมดนั้น
                ratios = []
                for test_name, data in valid_results.items():
                    base_time = baseline.get(test_name)
                    test_time = data["time"]
                    if base_time and test_time > 0:
                        ratios.append(base_time / test_time)
                if ratios:
                    avg_ratio = sum(ratios) / len(ratios)
                    if avg_ratio < 0.2:
                        msg = f"ผลการทดสอบ {test_type.upper()} ({mode}):\n\nไม่เหมาะสมสำหรับงาน AI/Program\n\n(ช้ากว่า baseline {1/avg_ratio:.1f} เท่า)"
                        root.after(0, lambda: msgbox.showerror("Performance Alert", msg))
                    elif 0.2 <= avg_ratio < 0.25:
                        msg = f"ผลการทดสอบ {test_type.upper()} ({mode}):\n\nความเหมาะสมปานกลาง\n\n(เร็วกว่า baseline {avg_ratio:.2f} เท่า)"
                        root.after(0, lambda: msgbox.showwarning("Performance Alert", msg))
                    else:
                        msg = f"ผลการทดสอบ {test_type.upper()} ({mode}):\n\nเหมาะสมเป็นอย่างมากสำหรับงาน AI/Program\n\n(เร็วกว่า baseline {avg_ratio:.2f} เท่า)"
                        root.after(0, lambda: msgbox.showinfo("Performance Alert", msg))

                try:
                    device = tab_utils.master.ai_test_device.get() if test_type == "ai" else tab_utils.master.pg_test_device.get()
                    cpu_brand = None
                    cpu_info = None
                    try:
                        import pythoncom
                        pythoncom.CoInitialize()
                        cpu_brand = platform.processor()
                        c = wmi.WMI()
                        cpu_list = c.Win32_Processor()
                        if cpu_list:
                            cpu_info = cpu_list[0].Name
                    except Exception as cpu_e:
                        logging.warning(f"Cannot get CPU info: {cpu_e}")
                    scores_dict = {k: v for k, v in valid_results.items()}
                    tab_utils.db.insert_benchmark_log(
                        test_type, total_time, avg_score, device, mode,
                        cpu_brand=cpu_brand, cpu_info=cpu_info, scores_dict=scores_dict
                    )
                    logging.debug(f"Sent benchmark log to API for {test_type} in {mode} mode")
                except Exception as e:
                    error_msg = f"Error inserting benchmark log: {str(e)}"
                    logging.error(error_msg)
                    root.after(0, lambda msg=f"{error_msg}\n": output_widget.insert(tk.END, msg))

                if callback and callable(callback):
                    root.after(0, lambda: callback())

                if baseline_updated:
                    save_baseline(baseline, device_type, mode, test_type)

            except Exception as e:
                error_msg = f"Error in run_all_tests: {str(e)}\n{traceback.format_exc()}"
                logging.error(error_msg)
                root.after(0, lambda msg=f"Error: {str(e)}\n": output_widget.insert(tk.END, msg))
                root.after(0, lambda: output_widget.see(tk.END))
            if baseline_updated:
                save_baseline(baseline, device_type, mode, test_type)

        test_thread = threading.Thread(target=run_all_tests, daemon=True)
        test_thread.start()

    except Exception as e:
        error_msg = f"Error in start_tests: {str(e)}\n{traceback.format_exc()}"
        logging.error(error_msg)
        root.after(0, lambda msg=f"Error: {str(e)}\n": output_widget.insert(tk.END, msg))
        root.after(0, lambda: output_widget.see(tk.END))