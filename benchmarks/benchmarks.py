import os
import sys

# Исправление для Tcl/Tk на Windows
project_path = r"C:\Users\idaku\PycharmProjects\9lab"
os.environ['TCL_LIBRARY'] = os.path.join(project_path, '.venv', 'Lib', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(project_path, '.venv', 'Lib', 'tk8.6')
import time
import statistics

# Добавляем пути для импорта
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'python-client'))

from http_client import GoHTTPClient
from rust_processor import DataProcessor


def benchmark_python_sum_of_squares(numbers):
    """Чистый Python: сумма квадратов"""
    start = time.perf_counter()
    result = sum(n * n for n in numbers)
    elapsed = (time.perf_counter() - start) * 1000
    return result, elapsed


def benchmark_python_multiply(numbers, factor=2):
    """Чистый Python: умножение каждого числа на factor"""
    start = time.perf_counter()
    result = [n * factor for n in numbers]
    elapsed = (time.perf_counter() - start) * 1000
    return result, elapsed


def benchmark_rust_multiply(numbers, factor=2):
    """Python + Rust: умножение через DataProcessor"""
    processor = DataProcessor(factor)
    start = time.perf_counter()
    result = processor.process(numbers)
    elapsed = (time.perf_counter() - start) * 1000
    return result, elapsed


def benchmark_go_sum_of_squares(numbers):
    """Python + Go HTTP: сумма квадратов через HTTP-сервер"""
    client = GoHTTPClient()
    start = time.perf_counter()
    result = client.compute(numbers)
    elapsed = (time.perf_counter() - start) * 1000

    if result["success"]:
        return result["result"], elapsed
    else:
        return None, elapsed


def run_benchmarks():
    """Запуск всех бенчмарков"""
    sizes = [100, 500, 1000, 5000, 10000, 50000]

    results = {
        "python_sum": {"times": [], "results": []},
        "python_multiply": {"times": [], "results": []},
        "rust_multiply": {"times": [], "results": []},
        "go_sum": {"times": [], "results": []}
    }

    print("=" * 80)
    print("BENCHMARK: Performance Comparison")
    print("Python vs Rust (PyO3) vs Go (HTTP)")
    print("=" * 80)
    print(f"{'Size':<10} {'Python Sum (ms)':<18} {'Python Mul (ms)':<18} {'Rust Mul (ms)':<18} {'Go Sum (ms)':<15}")
    print("-" * 80)

    for size in sizes:
        numbers = list(range(1, size + 1))

        # Python: сумма квадратов
        _, py_sum_time = benchmark_python_sum_of_squares(numbers)
        results["python_sum"]["times"].append(py_sum_time)

        # Python: умножение
        _, py_mul_time = benchmark_python_multiply(numbers, 2)
        results["python_multiply"]["times"].append(py_mul_time)

        # Rust: умножение
        _, rust_time = benchmark_rust_multiply(numbers, 2)
        results["rust_multiply"]["times"].append(rust_time)

        # Go: сумма квадратов через HTTP
        try:
            _, go_time = benchmark_go_sum_of_squares(numbers)
            results["go_sum"]["times"].append(go_time)
            go_display = f"{go_time:.2f}"
        except Exception as e:
            print(f"Go server error for size {size}: {e}")
            results["go_sum"]["times"].append(None)
            go_display = "N/A"

        print(
            f"{size:<10} {py_sum_time:.4f}{' ' * 11} {py_mul_time:.4f}{' ' * 11} {rust_time:.4f}{' ' * 11} {go_display}")

    print("=" * 80)

    # Статистика
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    avg_py_sum = statistics.mean(results["python_sum"]["times"])
    avg_py_mul = statistics.mean(results["python_multiply"]["times"])
    avg_rust = statistics.mean(results["rust_multiply"]["times"])

    print(f"Python (sum of squares) average: {avg_py_sum:.2f} ms")
    print(f"Python (multiply) average:       {avg_py_mul:.2f} ms")
    print(f"Rust (multiply) average:         {avg_rust:.2f} ms")
    print(f"Speedup Rust vs Python (multiply): {avg_py_mul / avg_rust:.2f}x")

    go_times = [t for t in results["go_sum"]["times"] if t is not None]
    if go_times:
        avg_go = statistics.mean(go_times)
        print(f"Go (sum of squares) average:    {avg_go:.2f} ms")
        print(f"Speedup Go vs Python (sum):      {avg_py_sum / avg_go:.2f}x")

    # Сравнение Rust умножение vs Python умножение
    print("\n" + "-" * 40)
    print("Rust vs Python (multiplication):")
    print(f"  Python slower by: {avg_py_mul - avg_rust:.2f} ms")
    print(f"  Rust faster by:   {avg_py_mul / avg_rust:.2f}x")

    return results, sizes


def save_results(results, sizes):
    """Сохранить результаты в JSON"""
    import json

    output = {
        "sizes": sizes,
        "python_sum_times_ms": results["python_sum"]["times"],
        "python_multiply_times_ms": results["python_multiply"]["times"],
        "rust_multiply_times_ms": results["rust_multiply"]["times"],
        "go_sum_times_ms": [t for t in results["go_sum"]["times"] if t is not None]
    }

    filepath = os.path.join(os.path.dirname(__file__), 'benchmark_results.json')
    with open(filepath, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\nResults saved to: {filepath}")


def plot_results(results, sizes):
    """Построить график (если matplotlib установлен)"""
    try:
        import matplotlib.pyplot as plt

        plt.figure(figsize=(12, 7))

        plt.plot(sizes, results["python_sum"]["times"], 'o-',
                 label='Python (sum of squares)', linewidth=2, markersize=8, color='blue')
        plt.plot(sizes, results["python_multiply"]["times"], 's-',
                 label='Python (multiply)', linewidth=2, markersize=8, color='cyan')
        plt.plot(sizes, results["rust_multiply"]["times"], '^-',
                 label='Rust (multiply via PyO3)', linewidth=2, markersize=8, color='green')

        go_times = [t if t is not None else float('nan') for t in results["go_sum"]["times"]]
        plt.plot(sizes, go_times, 'D-',
                 label='Go (sum via HTTP)', linewidth=2, markersize=8, color='orange')

        plt.xlabel('Dataset Size (number of elements)', fontsize=12)
        plt.ylabel('Execution Time (ms)', fontsize=12)
        plt.title('Performance Comparison: Python vs Rust vs Go', fontsize=14)
        plt.legend(fontsize=10)
        plt.grid(True, alpha=0.3)
        plt.xscale('log')
        plt.yscale('log')

        # Сохраняем график
        filepath = os.path.join(os.path.dirname(__file__), 'benchmark_results.png')
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        print(f"Graph saved to: {filepath}")

        plt.show()

    except ImportError:
        print("\n⚠️  matplotlib not installed. Install with: pip install matplotlib")
    except Exception as e:
        print(f"\nCould not plot graph: {e}")


def main():
    print("\n⚠️  IMPORTANT: Make sure Go HTTP server is running!")
    print("   Run in separate terminal: cd go-http-service && go run main.go\n")

    response = input("Press Enter to start benchmarks (or 's' to skip Go server)... ")

    results, sizes = run_benchmarks()

    save_results(results, sizes)
    plot_results(results, sizes)

    print("\n" + "=" * 80)
    print("CONCLUSIONS")
    print("=" * 80)
    print("1. Rust (PyO3) is significantly faster than Python for number processing")
    print("2. Go HTTP service has overhead due to network communication")
    print("3. For CPU-bound tasks, Rust is the best choice")
    print("4. Go is good for network services but adds latency for simple computations")


if __name__ == "__main__":
    main()