# Language Performance Comparison

A comprehensive benchmark testing tool to compare the multithreading performance of 10 programming languages: Python, Go, Java, C, C++, C#, PHP, Ruby, JavaScript, and TypeScript.

## Overview

This project provides a standardized benchmark to measure and compare the computational performance of different programming languages using a CPU-intensive task (prime number calculation). Each language implementation uses its native multithreading capabilities (or single-threaded execution where multithreading is not available).

## Supported Languages

| Language | Threading Model | Notes |
|----------|----------------|-------|
| Python | Threading (GIL limited) | Uses `threading` module |
| Go | Goroutines | Native concurrency model |
| Java | Multithreading | Uses `ExecutorService` |
| C | POSIX Threads | Uses `pthread` library |
| C++ | std::thread | C++11 threading |
| C# | Task Parallel Library | Uses `Task` API |
| PHP | Single-threaded | No native multithreading |
| Ruby | Threading | Native thread support |
| JavaScript | Worker Threads | Node.js worker threads |
| TypeScript | Worker Threads | Compiled to JS with worker threads |

**Note:** HTML and CSS are markup/styling languages without computational capabilities, so they are not included in the benchmark.

## Benchmark Task

The benchmark measures computational throughput by continuously calculating prime numbers for a fixed duration (default: 1 second):
1. Each thread continuously finds prime numbers starting from 2
2. All threads run in parallel for the specified duration
3. Results report total primes found and primes per second (throughput)

This duration-based approach ensures meaningful comparison by:
- Running each language for the same amount of time (~1 second)
- Measuring actual computational throughput (primes/second)
- Avoiding the issue of very short execution times that make comparison difficult

## Requirements

### General
- Bash shell (for running the main script)
- Python 3 (for analysis script)

### Language-Specific
- **Python**: Python 3.6+
- **Go**: Go 1.11+
- **Java**: JDK 8+ with `javac` and `java`
- **C**: GCC compiler with pthread support
- **C++**: G++ compiler with C++11 support
- **C#**: .NET SDK or Mono
- **PHP**: PHP 7.0+
- **Ruby**: Ruby 2.0+
- **JavaScript**: Node.js 12+
- **TypeScript**: Node.js 12+ and TypeScript (`npm install -g typescript`)

You don't need all languages installed - the benchmark script will automatically skip any that are not available.

## Installation

1. Clone this repository:
```bash
git clone https://github.com/JimmyKodu/LanguagePerformanceComparison.git
cd LanguagePerformanceComparison
```

2. Make sure the required languages are installed on your system (install only what you want to test)

3. Make scripts executable (should already be done):
```bash
chmod +x run_benchmarks.sh analyze_results.py
```

## Usage

### Running Benchmarks

Run all available benchmarks with default settings (4 threads, 1 second duration):
```bash
./run_benchmarks.sh
```

Run with custom thread count and duration:
```bash
./run_benchmarks.sh <threads> <duration_seconds>

# Example: Use 8 threads and run for 2 seconds
./run_benchmarks.sh 8 2.0

# Example: Use 2 threads and run for 0.5 seconds  
./run_benchmarks.sh 2 0.5
```

### Validating Implementations

To verify all benchmark implementations are working correctly:
```bash
./validate_benchmarks.py
```

This will run each language's benchmark with a small dataset and verify they all produce the correct prime count.

### Analyzing Results

After running benchmarks, analyze and compare the results:
```bash
./analyze_results.py
```

The analysis tool will display:
- Comparison table sorted by throughput (primes per second)
- Statistical analysis (fastest, slowest, average throughput)
- Multithreading analysis for each language

### Results

Results are saved as JSON files in the `results/` directory:
- `results/python.json`
- `results/go.json`
- `results/java.json`
- ... (one file per language)

Each result file contains:
```json
{
  "language": "Language Name",
  "threads": 4,
  "duration_seconds": 1.0,
  "actual_time_seconds": 1.002345,
  "primes_found": 1223039,
  "primes_per_second": 1220598
}
```

## Example Output

```
====================================================================================================
BENCHMARK RESULTS COMPARISON
====================================================================================================

Test Configuration:
  Duration: 1.0s

Language        Threads    Primes Found    Primes/sec      Performance
----------------------------------------------------------------------------------------------------
C               4          1224786         1223925         1.00x (fastest)
C++             4          1223317         1222782         1.00x
C#              4          1213296         1209054         0.99x
Java            4          1212854         1207860         0.99x
JavaScript      4          1217082         1170271         0.96x
TypeScript      4          1216515         1167480         0.95x
Go              4          1099974         1099654         0.90x
Python          4          102779          98154           0.08x
Ruby            4          86148           66195           0.05x
PHP             1          51636           51577           0.04x
----------------------------------------------------------------------------------------------------
```

## Project Structure

```
LanguagePerformanceComparison/
├── README.md                      # This file
├── run_benchmarks.sh              # Main benchmark runner
├── analyze_results.py             # Results analysis tool
├── benchmarks/                    # Benchmark implementations
│   ├── python/benchmark.py
│   ├── go/benchmark.go
│   ├── java/Benchmark.java
│   ├── c/benchmark.c
│   ├── cpp/benchmark.cpp
│   ├── csharp/Benchmark.cs
│   ├── php/benchmark.php
│   ├── ruby/benchmark.rb
│   ├── javascript/
│   │   ├── benchmark.js
│   │   └── worker.js
│   └── typescript/
│       ├── benchmark.ts
│       └── worker.ts
└── results/                       # Benchmark results (generated)
    └── *.json
```

## Implementation Details

### Algorithm
All implementations use the same prime-checking algorithm for fair comparison:
- Trial division method
- Optimized to check only odd numbers after 2
- Checks divisors up to √n

### Fairness Considerations
- Same algorithm across all languages
- Same computational task (prime number calculation)  
- Fixed duration (1 second by default) ensures meaningful execution time
- Results based on throughput (primes/second) for clear comparison
- No language-specific optimizations
- Results include actual execution time for verification
- Fixed duration (1 second by default) ensures meaningful execution time
- Results based on throughput (primes/second) for clear comparison
- No language-specific optimizations
- Results include actual execution time for verification

### Limitations
- Python's Global Interpreter Lock (GIL) limits true parallel execution
- PHP lacks native multithreading support
- Performance depends on system resources and current load
- Compiled languages have an inherent advantage over interpreted ones
- Results may vary between runs and systems
- Very short durations (<0.5s) may show startup overhead effects

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests to:
- Add more languages
- Improve implementations
- Add new benchmark tasks
- Enhance analysis tools

## License

MIT License - feel free to use and modify as needed.

## Acknowledgments

This project demonstrates language performance characteristics for educational purposes. Real-world performance depends on many factors including the specific use case, libraries used, and optimization techniques applied.