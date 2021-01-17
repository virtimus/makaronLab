import concurrent.futures
import sys
import time

import wqc

try:
    COUNT = int(sys.argv[1])
except (IndexError, ValueError):
    print('Usage: python3 main.py <count of numbers to sum>.')
    sys.exit(1)


def py_sum(number_of_steps: int) -> int:
    with concurrent.futures.ThreadPoolExecutor() as executor:
        thread1 = executor.submit(sum_thread, 0, number_of_steps//2)
        thread2 = executor.submit(sum_thread, number_of_steps//2, number_of_steps)
        result1 = thread1.result()
        result2 = thread2.result()
    return result1 + result2


def sum_thread(start: int, stop: int) -> int:
    i = s = 0
    for i in range(start, stop):
        s += i+1
    return s

print(f'Calculating {COUNT}')

start = time.time()
result = wqc.sum(COUNT)
stop = time.time()
print(f'wqc.sum({COUNT}) = {result}\tCalculated in {stop-start}s')
result = wqc.sum(COUNT)
print(f'wqc.sum({COUNT}) = {result}\tCalculated in {stop-start}s')

start = time.time()
result = py_sum(COUNT)
stop = time.time()
print(f'py_sum({COUNT}) = {result}\tCalculated in {stop-start}s')
