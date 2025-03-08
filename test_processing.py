import time
import multiprocessing
import concurrent.futures
import asyncio


# Функция для вычисления n-го числа Фибоначчи
def fibonacci(n: int) -> int:
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


# Многопроцессный подход
def run_multiprocessing(n, num_processes):
    start_time = time.time()
    with multiprocessing.Pool(processes=num_processes) as pool:
        results = pool.apply(fibonacci, (n,))
    end_time = time.time()
    return end_time - start_time


# Многопоточный подход
def run_multithreading(n, num_threads):
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(fibonacci, i) for i in range(n)]
        results = [f.result() for f in concurrent.futures.as_completed(futures)]
    end_time = time.time()
    return end_time - start_time


# Асинхронный подход
async def async_fibonacci(n: int) -> int:
    if n <= 1:
        return n
    return (await async_fibonacci(n - 1)) + (await async_fibonacci(n - 2))


async def run_asyncio(n):
    start_time = time.time()
    results = await async_fibonacci(n)
    end_time = time.time()
    return end_time - start_time


# Основная функция для запуска всех подходов
def main(n, num_processes, num_threads):
    print("Количество вычислений:", n)

    # Многопроцессный подход
    # mp_time = run_multiprocessing(n, num_processes)
    # print(f"Время выполнения с использованием multiprocessing: {mp_time:.2f} секунд")

    # Многопоточный подход
    mt_time = run_multithreading(n, num_threads)
    print(f"Время выполнения с использованием threading: {mt_time:.2f} секунд")

    # Асинхронный подход
    ay_time = asyncio.run(run_asyncio(n))
    print(f"Время выполнения с использованием asyncio: {ay_time:.2f} секунд")


if __name__ == "__main__":
    n = 30  # Количество вычислений
    num_processes = 8  # Количество процессов
    num_threads = 8  # Количество потоков

    main(n, num_processes, num_threads)
