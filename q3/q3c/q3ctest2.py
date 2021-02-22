import concurrent.futures
import sys
import time

import q3c

'''
try:
    COUNT = int(sys.argv[1])
except (IndexError, ValueError):
    print('Usage: python3 main.py <count of numbers to sum>.')
    sys.exit(1)
'''

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

def hex64(n):
    return hex (n & 0xffffffffffffffff) #[:-1]

COUNT=20

print(f'Calculating {COUNT}')

start = time.time()
result = q3c.sum(COUNT)
stop = time.time()
print(f'q3c.sum({COUNT}) = {result}\tCalculated in {stop-start}s')
result = q3c.sum(COUNT)
print(f'q3c.sum({COUNT}) = {result}\tCalculated in {stop-start}s')
result = q3c.sum(COUNT)
print(f'q3c.sum({COUNT}) = {result}\tCalculated in {stop-start}s')


#//result = q3c.c6502_init({"jajo":0})
result = q3c.c6502_init(345)

print(f'q3c.c6502_init():{result}')

cpuDict = q3c.c6502_open()
print(cpuDict)
cpuDict = q3c.c6502_open()
print(cpuDict)

pins = cpuDict['pins']
iv = cpuDict['iv']

print(f'q3c.c6502_open():{iv} {hex(pins)}')
#result = q3c.c6502_init2()

#print(result)
start = time.time()
for i in range(0,40,1):
    pins = q3c.c6502_calc(iv,pins)
    print(f'q3c.c6502_calc(result):{iv} {hex64(pins)}')
stop = time.time()
print(f'Calculated in {stop-start}s')

#ares = q3c.c6502_insp()

#print(dir(ares))

#for v in ares:
#    print(v)


#start = time.time()
#result = py_sum(COUNT)
#stop = time.time()
#print(f'py_sum({COUNT}) = {result}\tCalculated in {stop-start}s')
