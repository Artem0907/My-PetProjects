import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import asyncio
from typing import List, Tuple


# --------------------------------------------------
# Оптимизированная версия функции Фибоначчи
# --------------------------------------------------
def fibonacci(n: int) -> int:
    """Итеративная версия для избежания recursion limit и stack overflow"""
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


# --------------------------------------------------
# Многопроцессная обработка (для CPU-bound задач)
# --------------------------------------------------
def run_multiprocessing(n: int, workers: int) -> float:
    start = time.perf_counter()
    with ProcessPoolExecutor(max_workers=workers) as executor:
        # Распределяем задания между процессами
        futures = [executor.submit(fibonacci, n) for _ in range(workers)]
        results = [f.result() for f in futures]
    return time.perf_counter() - start


# --------------------------------------------------
# Многопоточная обработка (для I/O-bound задач)
# --------------------------------------------------
def run_multithreading(n: int, workers: int) -> float:
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(fibonacci, n) for _ in range(workers)]
        results = [f.result() for f in futures]
    return time.perf_counter() - start


# --------------------------------------------------
# Синхронная версия (базовый уровень)
# --------------------------------------------------
def run_sequential(n: int, workers: int) -> float:
    start = time.perf_counter()
    results = [fibonacci(n) for _ in range(workers)]
    return time.perf_counter() - start


# --------------------------------------------------
# Асинхронная версия (для I/O-bound с async/await)
# --------------------------------------------------
async def async_worker(n: int) -> int:
    return fibonacci(n)


async def run_async(n: int, workers: int) -> float:
    start = time.perf_counter()
    tasks = [async_worker(n) for _ in range(workers)]
    await asyncio.gather(*tasks)
    return time.perf_counter() - start


# --------------------------------------------------
# Анализ и визуализация результатов
# --------------------------------------------------
def analyze_results(results: List[Tuple[str, float]]):
    max_name_len = max(len(name) for name, _ in results)
    print("\nРезультаты производительности:")
    print("-" * (max_name_len + 13))

    for name, time in sorted(results, key=lambda x: x[1]):
        print(f"{name.rjust(max_name_len)} | {time:.4f} сек")


# --------------------------------------------------
# Основной блок
# --------------------------------------------------
if __name__ == "__main__":
    # Конфигурация теста
    N = 100_000  # Величина вычислений
    WORKERS = 8  # Количество параллельных задач
    TRIALS = 10  # Количество повторов

    # Тестируемые подходы
    approaches = {
        "Multiprocessing": run_multiprocessing,
        "Multithreading": run_multithreading,
        "Sequential": run_sequential,
        "Async": lambda n, w: asyncio.run(run_async(n, w)),
    }

    # Сбор метрик
    metrics = []
    for name, func in approaches.items():
        total_time = 0.0
        for _ in range(TRIALS):
            total_time += func(N, WORKERS)
        metrics.append((name, total_time / TRIALS))

    analyze_results(metrics)
