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

The benchmark calculates prime numbers up to a specified limit (default: 100,000) by:
1. Dividing the range into equal chunks
2. Processing each chunk in parallel (when multithreading is available)
3. Aggregating results and measuring execution time

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

Run all available benchmarks with default settings (4 threads, 100,000 max number):
```bash
./run_benchmarks.sh
```

Run with custom thread count and range:
```bash
./run_benchmarks.sh <threads> <max_number>

# Example: Use 8 threads and calculate primes up to 200,000
./run_benchmarks.sh 8 200000
```

### Analyzing Results

After running benchmarks, analyze and compare the results:
```bash
./analyze_results.py
```

The analysis tool will display:
- Comparison table sorted by execution time
- Statistical analysis (fastest, slowest, average times)
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
  "max_number": 100000,
  "primes_found": 9592,
  "time_seconds": 1.234567
}
```

## Example Output

```
================================================================================
BENCHMARK RESULTS COMPARISON
================================================================================

Test Configuration:
  Max Number: 100000

Language        Threads    Primes Found    Time (s)     Speed
--------------------------------------------------------------------------------
C++             4          9592            0.123456     1.00x (fastest)
C               4          9592            0.145678     0.85x
Go              4          9592            0.167890     0.73x
Java            4          9592            0.234567     0.53x
C#              4          9592            0.289012     0.43x
JavaScript      4          9592            0.345678     0.36x
TypeScript      4          9592            0.367890     0.34x
Ruby            4          9592            0.456789     0.27x
Python          4          9592            0.567890     0.22x
PHP             1          9592            1.234567     0.10x
--------------------------------------------------------------------------------
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
- Consistent input parameters
- No language-specific optimizations
- Results include actual prime count for verification

### Limitations
- Python's Global Interpreter Lock (GIL) limits true parallel execution
- PHP lacks native multithreading support
- Performance depends on system resources and current load
- Compiled languages have an inherent advantage over interpreted ones
- Results may vary between runs and systems

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