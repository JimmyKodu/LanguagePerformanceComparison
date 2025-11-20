# Example Usage and Results

This file contains example commands and typical results you can expect from the benchmark tool.

## Basic Usage

### Run with default settings (4 threads, 100,000 range)
```bash
./run_benchmarks.sh
```

### Run with custom thread count and range
```bash
# 8 threads, calculate primes up to 200,000
./run_benchmarks.sh 8 200000

# 2 threads, calculate primes up to 50,000  
./run_benchmarks.sh 2 50000
```

## Example Output

### Benchmark Execution
```
======================================
Language Performance Comparison
======================================
Threads: 4
Max Number: 50000
======================================

Running Python benchmark...
{
  "language": "Python",
  "threads": 4,
  "max_number": 50000,
  "primes_found": 5133,
  "time_seconds": 0.021747
}

Running Go benchmark...
{
  "language": "Go",
  "threads": 4,
  "max_number": 50000,
  "primes_found": 5133,
  "time_seconds": 0.000679
}

... (output continues for each language)
```

### Analysis Results

After running benchmarks, execute the analysis:
```bash
./analyze_results.py
```

Sample output:
```
================================================================================
BENCHMARK RESULTS COMPARISON
================================================================================

Test Configuration:
  Max Number: 50000

Language        Threads    Primes Found    Time (s)     Speed
--------------------------------------------------------------------------------
Go              4          5133            0.000679     1.00x (fastest)
C++             4          5133            0.000715     0.95x
C               4          5133            0.000934     0.73x
C#              4          5133            0.005638     0.12x
Java            4          5133            0.009615     0.07x
Python          4          5133            0.021747     0.03x
PHP             1          5133            0.038994     0.02x
JavaScript      4          5133            0.044000     0.02x
Ruby            4          5133            0.044169     0.02x
TypeScript      4          5133            0.045000     0.02x
--------------------------------------------------------------------------------

================================================================================
STATISTICAL ANALYSIS
================================================================================
Total languages tested: 10
Fastest time: 0.000679 seconds
Slowest time: 0.045000 seconds
Average time: 0.021149 seconds
Speed difference (slowest/fastest): 66.24x

================================================================================
MULTITHREADING ANALYSIS
================================================================================
C               4 threads utilized
C#              4 threads utilized
C++             4 threads utilized
Go              4 threads utilized
Java            4 threads utilized
JavaScript      4 threads utilized
PHP             Single-threaded execution
Python          4 threads utilized
Ruby            4 threads utilized
TypeScript      4 threads utilized
```

## Performance Insights

Based on typical runs:

1. **Fastest**: Compiled languages with native threading
   - Go: Excellent concurrency with goroutines
   - C++: Low-level control with std::thread
   - C: Efficient pthread implementation

2. **Mid-tier**: Managed runtime languages
   - C#: Good performance with Task Parallel Library
   - Java: Solid multithreading but JVM startup overhead

3. **Slower**: Interpreted languages
   - Python: Limited by GIL (Global Interpreter Lock)
   - Ruby: Threading overhead in interpreter
   - JavaScript/TypeScript: Worker thread overhead
   - PHP: Single-threaded only

## Verification

All implementations should produce the same prime count for the same range:
- Up to 5,000: 669 primes
- Up to 10,000: 1,229 primes
- Up to 50,000: 5,133 primes
- Up to 100,000: 9,592 primes

If any language produces different counts, there's an implementation bug.

## Tips for Accurate Benchmarking

1. **Close other applications** to reduce system load
2. **Run multiple times** and average the results
3. **Use larger ranges** (e.g., 500,000+) for more significant differences
4. **Disable CPU throttling** if measuring absolute performance
5. **Consider compilation flags** - results shown use -O2 optimization for C/C++

## Running Individual Benchmarks

You can run each language's benchmark individually:

```bash
# Python
python3 benchmarks/python/benchmark.py 4 100000

# Go
cd benchmarks/go && go run benchmark.go 4 100000

# Java
cd benchmarks/java && javac Benchmark.java && java Benchmark 4 100000

# C
cd benchmarks/c && gcc -o benchmark benchmark.c -pthread -lm -O2 && ./benchmark 4 100000

# C++
cd benchmarks/cpp && g++ -o benchmark benchmark.cpp -pthread -O2 -std=c++11 && ./benchmark 4 100000

# C#
cd benchmarks/csharp/Benchmark && dotnet run -c Release -- 4 100000

# PHP (always single-threaded)
php benchmarks/php/benchmark.php 4 100000

# Ruby
ruby benchmarks/ruby/benchmark.rb 4 100000

# JavaScript
node benchmarks/javascript/benchmark.js 4 100000

# TypeScript
cd benchmarks/typescript && tsc && node benchmark.js 4 100000
```
