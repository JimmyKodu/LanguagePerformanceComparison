#!/usr/bin/env python3
"""
Python multithreading benchmark
Calculates prime numbers using multiple threads for a fixed duration
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

def count_primes_for_duration(duration, results, index, stop_flag):
    """Count prime numbers for a given duration"""
    count = 0
    num = 2
    start_time = time.time()
    
    while not stop_flag[0]:
        if is_prime(num):
            count += 1
        num += 1
        
        # Check time periodically (every 1000 numbers to reduce overhead)
        if num % 1000 == 0:
            if time.time() - start_time >= duration:
                break
    
    results[index] = count

def benchmark(num_threads=4, duration=1.0):
    """Run the benchmark with specified number of threads for a fixed duration"""
    start_time = time.time()
    
    threads = []
    results = [0] * num_threads
    stop_flag = [False]
    
    for i in range(num_threads):
        thread = threading.Thread(target=count_primes_for_duration, args=(duration, results, i, stop_flag))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    total_primes = sum(results)
    end_time = time.time()
    actual_time = end_time - start_time
    
    return {
        "language": "Python",
        "threads": num_threads,
        "duration_seconds": duration,
        "actual_time_seconds": actual_time,
        "primes_found": total_primes,
        "primes_per_second": int(total_primes / actual_time)
    }

if __name__ == "__main__":
    num_threads = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    duration = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
    
    result = benchmark(num_threads, duration)
    print(json.dumps(result, indent=2))
