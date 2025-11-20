#!/usr/bin/env python3
"""
Analyze and compare benchmark results from different programming languages
"""
import json
import os
import sys
from pathlib import Path

def load_results(results_dir):
    """Load all benchmark results from JSON files"""
    results = []
    results_path = Path(results_dir)
    
    if not results_path.exists():
        print(f"Results directory not found: {results_dir}")
        return results
    
    for json_file in results_path.glob("*.json"):
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
                results.append(data)
        except Exception as e:
            print(f"Error loading {json_file}: {e}")
    
    return results

def print_comparison_table(results):
    """Print a formatted comparison table"""
    if not results:
        print("No results to compare")
        return
    
    # Sort by primes_per_second (fastest first)
    sorted_results = sorted(results, key=lambda x: x.get('primes_per_second', 0), reverse=True)
    
    print("\n" + "="*100)
    print("BENCHMARK RESULTS COMPARISON")
    print("="*100)
    print(f"\nTest Configuration:")
    if sorted_results:
        print(f"  Duration: {sorted_results[0].get('duration_seconds', 'N/A')}s")
    print()
    
    # Header
    print(f"{'Language':<15} {'Threads':<10} {'Primes Found':<15} {'Primes/sec':<15} {'Performance'}")
    print("-"*100)
    
    # Get fastest primes/sec for relative performance calculation
    fastest_rate = sorted_results[0].get('primes_per_second', 1)
    
    # Print each result
    for i, result in enumerate(sorted_results, 1):
        language = result.get('language', 'Unknown')
        threads = result.get('threads', 'N/A')
        primes = result.get('primes_found', 'N/A')
        primes_per_sec = result.get('primes_per_second', 'N/A')
        
        # Calculate relative performance
        if isinstance(primes_per_sec, (int, float)) and primes_per_sec > 0:
            relative_perf = f"{primes_per_sec/fastest_rate:.2f}x"
            if i == 1:
                relative_perf = "1.00x (fastest)"
        else:
            relative_perf = "N/A"
        
        print(f"{language:<15} {str(threads):<10} {str(primes):<15} {str(primes_per_sec):<15} {relative_perf}")
    
    print("-"*100)
    print()

def print_statistics(results):
    """Print statistical analysis"""
    if not results:
        return
    
    rates = [r.get('primes_per_second') for r in results if 'primes_per_second' in r]
    
    if not rates:
        return
    
    print("\n" + "="*100)
    print("STATISTICAL ANALYSIS")
    print("="*100)
    print(f"Total languages tested: {len(results)}")
    print(f"Fastest throughput: {max(rates):,} primes/second")
    print(f"Slowest throughput: {min(rates):,} primes/second")
    print(f"Average throughput: {int(sum(rates)/len(rates)):,} primes/second")
    print(f"Performance difference (fastest/slowest): {max(rates)/min(rates):.2f}x")
    print()

def print_multithreading_analysis(results):
    """Analyze multithreading effectiveness"""
    print("\n" + "="*100)
    print("MULTITHREADING ANALYSIS")
    print("="*100)
    
    for result in sorted(results, key=lambda x: x.get('language', '')):
        language = result.get('language', 'Unknown')
        threads = result.get('threads', 1)
        
        if threads == 1:
            print(f"{language:<15} Single-threaded execution")
        else:
            print(f"{language:<15} {threads} threads utilized")
    
    print()

def main():
    script_dir = Path(__file__).parent
    results_dir = script_dir / "results"
    
    # Allow custom results directory as argument
    if len(sys.argv) > 1:
        results_dir = Path(sys.argv[1])
    
    print("\nLoading benchmark results...")
    results = load_results(results_dir)
    
    if not results:
        print("No benchmark results found. Please run benchmarks first using run_benchmarks.sh")
        sys.exit(1)
    
    print(f"Found {len(results)} benchmark result(s)")
    
    # Print all analyses
    print_comparison_table(results)
    print_statistics(results)
    print_multithreading_analysis(results)
    
    print("="*100)
    print("Analysis complete!")
    print("="*100)
    print()

if __name__ == "__main__":
    main()
