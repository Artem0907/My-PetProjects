from time import time
from multiprocessing import Pool as mp_Pool
from threading import Thread
from asyncio import get_event_loop
from functools import cache


# Функция для вычисления n-го числа Фибоначчи
def fibonacci(n: int) -> int:
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


# Многопроцессный подход
def run_multiprocessing(n, num_processes):
    start_time = time()
    with mp_Pool(processes=num_processes) as pool:
        results = pool.apply(fibonacci, (n,))
    end_time = time()
    return end_time - start_time


# Многопоточный подход
def run_multithreading(n, num_threads):
    start_time = time()
    threads = []
    for thread_id in range(num_threads):
        threads.append(Thread(target=fibonacci, args=(n,)))
    for thread_id in threads:
        thread_id.start()
    for thread_id in threads:
        thread_id.join()
    end_time = time()
    return end_time - start_time


# Стандартный подход
def run_standard(n):
    start_time = time()
    results = fibonacci(n)
    end_time = time()
    return end_time - start_time


# Асинхронный подход
async def async_fibonacci(n: int) -> int:
    if n <= 1:
        return n
    return (await async_fibonacci(n - 1)) + (await async_fibonacci(n - 2))


async def run_asyncio(n):
    start_time = time()
    results = await async_fibonacci(n)
    end_time = time()
    return end_time - start_time


# Кэшированный подход
def run_cached(n):
    start_time = time()
    cache(fibonacci)(n)
    end_time = time()
    return end_time - start_time


# Основная функция для запуска всех подходов
def main(iters, n, num_processes, num_threads):
    async_loop = get_event_loop()
    print("Количество повторений:", iters)
    print("Количество вычислений:", n)

    mp_time = []
    mt_time = []
    sd_time = []
    ay_time = []
    ch_time = []

    for i in range(iters):
        # Многопроцессный подход
        mp_time.append(run_multiprocessing(n, num_processes))

        # Многопоточный подход
        mt_time.append(run_multithreading(n, num_threads))

        # Стандартный подход
        sd_time.append(run_standard(n))

        # Асинхронный подход
        ay_time.append(async_loop.run_until_complete(run_asyncio(n)))

        # Кэшированный подход
        ch_time.append(run_cached(n))

    approach = [
        ("multiprocessing", sum(mp_time) / iters),
        ("threading", sum(mt_time) / iters),
        ("standard", sum(sd_time) / iters),
        ("asyncio", sum(ay_time) / iters),
        ("cache", sum(ch_time) / iters),
    ]
    max_len = max(map(lambda el: len(el[0]), approach))

    print(
        "Время выполнения",
        *map(
            lambda el: f"    {' '*(max_len-len(el[0]))}{el[0]}:  {el[1]:.2f}",
            sorted(
                approach,
                key=lambda _t: _t[1],
            ),
        ),
        sep="\n",
    )


if __name__ == "__main__":
    iters = 10  # Количество повторений
    n = 30  # Количество вычислений
    num_processes = 8  # Количество процессов
    num_threads = 8  # Количество потоков

    main(iters, n, num_processes, num_threads)
