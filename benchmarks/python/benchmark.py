#!/usr/bin/env python3
"""
Python multithreading benchmark
Calculates prime numbers using multiple threads
"""
import time
import threading
import sys
import json

def is_prime(n):
    """Check if a number is prime"""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

def count_primes_in_range(start, end, results, index):
    """Count prime numbers in a given range"""
    count = 0
    for num in range(start, end):
        if is_prime(num):
            count += 1
    results[index] = count

def benchmark(num_threads=4, max_number=100000):
    """Run the benchmark with specified number of threads"""
    start_time = time.time()
    
    # Divide work among threads
    chunk_size = max_number // num_threads
    threads = []
    results = [0] * num_threads
    
    for i in range(num_threads):
        start = i * chunk_size
        end = (i + 1) * chunk_size if i < num_threads - 1 else max_number
        thread = threading.Thread(target=count_primes_in_range, args=(start, end, results, i))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    total_primes = sum(results)
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    return {
        "language": "Python",
        "threads": num_threads,
        "max_number": max_number,
        "primes_found": total_primes,
        "time_seconds": elapsed_time
    }

if __name__ == "__main__":
    num_threads = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    max_number = int(sys.argv[2]) if len(sys.argv) > 2 else 100000
    
    result = benchmark(num_threads, max_number)
    print(json.dumps(result, indent=2))
