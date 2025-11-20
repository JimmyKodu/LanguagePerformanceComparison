#!/usr/bin/env python3
"""
Validation script to ensure all benchmark implementations produce correct results
"""
import json
import subprocess
import sys
from pathlib import Path

# Expected prime counts for various ranges
EXPECTED_PRIMES = {
    5000: 669,
    10000: 1229,
    50000: 5133,
    100000: 9592
}

def run_benchmark(language, command, threads=2, max_number=5000):
    """Run a single benchmark and return the result"""
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=30,
            shell=True
        )
        
        if result.returncode != 0:
            return None, f"Failed with exit code {result.returncode}"
        
        # Parse JSON output
        output = result.stdout.strip()
        # If stdout is empty, might be in stderr (some tools output to stderr)
        if not output:
            output = result.stderr.strip()
        
        data = json.loads(output)
        
        return data, None
        
    except subprocess.TimeoutExpired:
        return None, "Timeout"
    except json.JSONDecodeError as e:
        return None, f"JSON parse error: {e}"
    except Exception as e:
        return None, str(e)

def main():
    script_dir = Path(__file__).parent
    benchmarks_dir = script_dir / "benchmarks"
    
    test_threads = 2
    test_range = 5000
    expected_primes = EXPECTED_PRIMES[test_range]
    
    print("="*80)
    print("BENCHMARK VALIDATION TEST")
    print("="*80)
    print(f"Testing with {test_threads} threads, range up to {test_range}")
    print(f"Expected prime count: {expected_primes}")
    print("="*80)
    print()
    
    tests = [
        ("Python", f"python3 {benchmarks_dir}/python/benchmark.py {test_threads} {test_range}"),
        ("Go", f"cd {benchmarks_dir}/go && go run benchmark.go {test_threads} {test_range}"),
        ("Java", f"cd {benchmarks_dir}/java && javac Benchmark.java 2>/dev/null && java Benchmark {test_threads} {test_range}"),
        ("C", f"cd {benchmarks_dir}/c && gcc -o benchmark benchmark.c -pthread -lm -O2 2>/dev/null && ./benchmark {test_threads} {test_range}"),
        ("C++", f"cd {benchmarks_dir}/cpp && g++ -o benchmark benchmark.cpp -pthread -O2 -std=c++11 2>/dev/null && ./benchmark {test_threads} {test_range}"),
        ("C#", f"cd {benchmarks_dir}/csharp/Benchmark && dotnet run -c Release -- {test_threads} {test_range} 2>/dev/null"),
        ("PHP", f"php {benchmarks_dir}/php/benchmark.php {test_threads} {test_range}"),
        ("Ruby", f"ruby {benchmarks_dir}/ruby/benchmark.rb {test_threads} {test_range}"),
        ("JavaScript", f"node {benchmarks_dir}/javascript/benchmark.js {test_threads} {test_range}"),
        ("TypeScript", f"cd {benchmarks_dir}/typescript && tsc 2>/dev/null && node benchmark.js {test_threads} {test_range}"),
    ]
    
    passed = 0
    failed = 0
    skipped = 0
    
    for language, command in tests:
        print(f"Testing {language}...", end=" ")
        result, error = run_benchmark(language, command, test_threads, test_range)
        
        if error:
            print(f"❌ FAILED: {error}")
            failed += 1
        elif result:
            primes_found = result.get('primes_found', 0)
            if primes_found == expected_primes:
                print(f"✓ PASSED (found {primes_found} primes)")
                passed += 1
            else:
                print(f"❌ FAILED: Expected {expected_primes}, got {primes_found}")
                failed += 1
        else:
            print("⊘ SKIPPED")
            skipped += 1
    
    print()
    print("="*80)
    print("VALIDATION SUMMARY")
    print("="*80)
    print(f"Passed:  {passed}")
    print(f"Failed:  {failed}")
    print(f"Skipped: {skipped}")
    print(f"Total:   {passed + failed + skipped}")
    print("="*80)
    
    if failed > 0:
        print("\n⚠️  Some tests failed. Please check the implementations.")
        sys.exit(1)
    else:
        print("\n✓ All tests passed!")
        sys.exit(0)

if __name__ == "__main__":
    main()
