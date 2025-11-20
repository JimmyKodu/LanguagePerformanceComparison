#!/bin/bash

# Benchmark Runner Script
# Compiles and runs benchmarks for all languages

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BENCHMARK_DIR="$SCRIPT_DIR/benchmarks"
RESULTS_DIR="$SCRIPT_DIR/results"

# Default parameters
THREADS=${1:-4}
DURATION=${2:-1.0}

echo "======================================"
echo "Language Performance Comparison"
echo "======================================"
echo "Threads: $THREADS"
echo "Duration: ${DURATION}s"
echo "======================================"
echo ""

# Create results directory
mkdir -p "$RESULTS_DIR"

# Python
echo "Running Python benchmark..."
if command -v python3 &> /dev/null; then
    python3 "$BENCHMARK_DIR/python/benchmark.py" "$THREADS" "$DURATION" | tee "$RESULTS_DIR/python.json"
    echo ""
else
    echo "Python3 not found, skipping..."
    echo ""
fi

# Go
echo "Running Go benchmark..."
if command -v go &> /dev/null; then
    cd "$BENCHMARK_DIR/go"
    go build -o benchmark benchmark.go
    ./benchmark "$THREADS" "$DURATION" | tee "$RESULTS_DIR/go.json"
    rm -f benchmark
    cd "$SCRIPT_DIR"
    echo ""
else
    echo "Go not found, skipping..."
    echo ""
fi

# Java
echo "Running Java benchmark..."
if command -v javac &> /dev/null && command -v java &> /dev/null; then
    cd "$BENCHMARK_DIR/java"
    # Try to compile with Gson if available, otherwise use simple version
    if javac -cp ".:*" Benchmark.java 2>/dev/null || javac Benchmark.java 2>/dev/null; then
        java -cp ".:*" Benchmark "$THREADS" "$DURATION" 2>/dev/null | tee "$RESULTS_DIR/java.json" || \
        java Benchmark "$THREADS" "$DURATION" | tee "$RESULTS_DIR/java.json"
        rm -f Benchmark.class PrimeCounter.class BenchmarkResult.class
    fi
    cd "$SCRIPT_DIR"
    echo ""
else
    echo "Java not found, skipping..."
    echo ""
fi

# C
echo "Running C benchmark..."
if command -v gcc &> /dev/null; then
    cd "$BENCHMARK_DIR/c"
    gcc -o benchmark benchmark.c -pthread -lm -O2
    ./benchmark "$THREADS" "$DURATION" | tee "$RESULTS_DIR/c.json"
    rm -f benchmark
    cd "$SCRIPT_DIR"
    echo ""
else
    echo "GCC not found, skipping..."
    echo ""
fi

# C++
echo "Running C++ benchmark..."
if command -v g++ &> /dev/null; then
    cd "$BENCHMARK_DIR/cpp"
    g++ -o benchmark benchmark.cpp -pthread -O2 -std=c++11
    ./benchmark "$THREADS" "$DURATION" | tee "$RESULTS_DIR/cpp.json"
    rm -f benchmark
    cd "$SCRIPT_DIR"
    echo ""
else
    echo "G++ not found, skipping..."
    echo ""
fi

# C#
echo "Running C# benchmark..."
if command -v dotnet &> /dev/null; then
    cd "$BENCHMARK_DIR/csharp/Benchmark"
    if [ -f "Benchmark.csproj" ]; then
        dotnet run -c Release --no-build -- "$THREADS" "$DURATION" 2>/dev/null | tee "$RESULTS_DIR/csharp.json" || \
        dotnet run -c Release -- "$THREADS" "$DURATION" 2>/dev/null | tee "$RESULTS_DIR/csharp.json"
    fi
    cd "$SCRIPT_DIR"
    echo ""
else
    echo "dotnet not found, skipping..."
    echo ""
fi

# PHP
echo "Running PHP benchmark..."
if command -v php &> /dev/null; then
    php "$BENCHMARK_DIR/php/benchmark.php" "$THREADS" "$DURATION" | tee "$RESULTS_DIR/php.json"
    echo ""
else
    echo "PHP not found, skipping..."
    echo ""
fi

# Ruby
echo "Running Ruby benchmark..."
if command -v ruby &> /dev/null; then
    ruby "$BENCHMARK_DIR/ruby/benchmark.rb" "$THREADS" "$DURATION" | tee "$RESULTS_DIR/ruby.json"
    echo ""
else
    echo "Ruby not found, skipping..."
    echo ""
fi

# JavaScript (Node.js)
echo "Running JavaScript benchmark..."
if command -v node &> /dev/null; then
    node "$BENCHMARK_DIR/javascript/benchmark.js" "$THREADS" "$DURATION" | tee "$RESULTS_DIR/javascript.json"
    echo ""
else
    echo "Node.js not found, skipping..."
    echo ""
fi

# TypeScript
echo "Running TypeScript benchmark..."
if command -v ts-node &> /dev/null; then
    ts-node "$BENCHMARK_DIR/typescript/benchmark.ts" "$THREADS" "$DURATION" | tee "$RESULTS_DIR/typescript.json"
    echo ""
elif command -v node &> /dev/null && command -v tsc &> /dev/null; then
    cd "$BENCHMARK_DIR/typescript"
    tsc benchmark.ts worker.ts
    node benchmark.js "$THREADS" "$DURATION" | tee "$RESULTS_DIR/typescript.json"
    rm -f benchmark.js worker.js
    cd "$SCRIPT_DIR"
    echo ""
else
    echo "TypeScript not found, skipping..."
    echo ""
fi

echo "======================================"
echo "Benchmarks completed!"
echo "Results saved in: $RESULTS_DIR"
echo "======================================"
