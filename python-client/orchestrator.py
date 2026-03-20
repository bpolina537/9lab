import sys
import os

# Добавляем путь для импорта модулей
sys.path.insert(0, os.path.dirname(__file__))

from http_client import GoHTTPClient
from rust_processor import DataProcessor


class Orchestrator:
    """
    Оркестратор, объединяющий Go HTTP-микросервис и Rust библиотеку.

    Задание 4: Python-приложение, которое использует:
    - Go-микросервис для оркестрации (вычисления суммы квадратов)
    - Rust-библиотеку для криптографии (в нашем случае - умножение на factor)
    """

    def __init__(self, go_url="http://localhost:8081", rust_factor=2):
        self.go_client = GoHTTPClient(go_url)
        self.rust_processor = DataProcessor(rust_factor)

    def process_pipeline(self, numbers):
        """
        Полный пайплайн обработки:
        1. Отправляем числа в Go-микросервис для вычисления суммы квадратов
        2. Полученный результат обрабатываем Rust-библиотекой (умножаем на factor)
        3. Возвращаем финальный результат
        """
        print(f"Step 1: Sending {len(numbers)} numbers to Go HTTP service...")
        go_result = self.go_client.compute(numbers)

        if not go_result["success"]:
            return {
                "success": False,
                "error": f"Go service failed: {go_result['error']}",
                "step": "go_compute"
            }

        print(f"Step 2: Go service returned sum of squares = {go_result['result']}")
        print(f"Step 3: Processing with Rust (multiplying by {self.rust_processor.get_factor()})...")

        # Rust processor принимает список чисел, а у нас одно число
        # Преобразуем число в список из одной цифры или используем как есть
        rust_input = [go_result["result"]]
        rust_output = self.rust_processor.process(rust_input)

        final_result = rust_output[0]

        return {
            "success": True,
            "sum_of_squares": go_result["result"],
            "go_server_time_ms": go_result["server_time_ms"],
            "go_client_time_ms": go_result["client_time_ms"],
            "rust_factor": self.rust_processor.get_factor(),
            "final_result": final_result,
            "formula": f"({go_result['result']}) * {self.rust_processor.get_factor()} = {final_result}"
        }

    def crypto_pipeline(self, text):
        """
        Альтернативный пайплайн для криптографии:
        1. Преобразуем текст в числа (ASCII коды)
        2. Отправляем в Go для агрегации
        3. Rust применяет хеш-подобную обработку
        """
        # Преобразуем текст в числа
        numbers = [ord(c) for c in text]

        print(f"Step 1: Converted '{text}' to numbers: {numbers[:5]}...")

        go_result = self.go_client.compute(numbers)

        if not go_result["success"]:
            return {
                "success": False,
                "error": go_result["error"]
            }

        # Rust применяет "криптографическое" преобразование
        rust_result = self.rust_processor.process([go_result["result"]])

        return {
            "success": True,
            "original_text": text,
            "sum_of_codes": go_result["result"],
            "final_hash": rust_result[0],
            "formula": f"hash = (sum(ASCII codes)) * {self.rust_processor.get_factor()}"
        }


def main():
    print("=" * 50)
    print("Orchestrator Demo - Task 4")
    print("Combining Go HTTP Service + Rust Processor")
    print("=" * 50)

    # Создаём оркестратор
    orchestrator = Orchestrator(rust_factor=3)

    # Тест 1: Базовый пайплайн
    print("\n" + "-" * 30)
    print("Test 1: Basic Pipeline")
    print("-" * 30)

    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    result = orchestrator.process_pipeline(numbers)

    if result["success"]:
        print(f"✓ Success!")
        print(f"  Input numbers: {numbers}")
        print(f"  Sum of squares: {result['sum_of_squares']}")
        print(f"  Rust factor: {result['rust_factor']}")
        print(f"  Final result: {result['final_result']}")
        print(f"  Formula: {result['formula']}")
        print(f"  Go server time: {result['go_server_time_ms']:.2f} ms")
    else:
        print(f"✗ Failed: {result['error']}")

    # Тест 2: Криптографический пайплайн
    print("\n" + "-" * 30)
    print("Test 2: Crypto Pipeline")
    print("-" * 30)

    text = "Hello, World!"
    result = orchestrator.crypto_pipeline(text)

    if result["success"]:
        print(f"✓ Success!")
        print(f"  Original text: '{result['original_text']}'")
        print(f"  Sum of ASCII codes: {result['sum_of_codes']}")
        print(f"  Final hash: {result['final_hash']}")
        print(f"  Formula: {result['formula']}")
    else:
        print(f"✗ Failed: {result['error']}")

    # Тест 3: Большие данные
    print("\n" + "-" * 30)
    print("Test 3: Large Dataset (100 numbers)")
    print("-" * 30)

    large_numbers = list(range(1, 101))
    result = orchestrator.process_pipeline(large_numbers)

    if result["success"]:
        print(f"✓ Success!")
        print(f"  Input: 100 numbers (1..100)")
        print(f"  Sum of squares: {result['sum_of_squares']}")
        print(f"  Final result: {result['final_result']}")
        print(f"  Go server time: {result['go_server_time_ms']:.2f} ms")
    else:
        print(f"✗ Failed: {result['error']}")


if __name__ == "__main__":
    main()