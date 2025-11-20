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
    
    # Sort by time (fastest first)
    sorted_results = sorted(results, key=lambda x: x.get('time_seconds', float('inf')))
    
    print("\n" + "="*80)
    print("BENCHMARK RESULTS COMPARISON")
    print("="*80)
    print(f"\nTest Configuration:")
    if sorted_results:
        print(f"  Max Number: {sorted_results[0].get('max_number', 'N/A')}")
    print()
    
    # Header
    print(f"{'Language':<15} {'Threads':<10} {'Primes Found':<15} {'Time (s)':<12} {'Speed'}")
    print("-"*80)
    
    # Get fastest time for relative speed calculation
    fastest_time = sorted_results[0].get('time_seconds', 1)
    
    # Print each result
    for i, result in enumerate(sorted_results, 1):
        language = result.get('language', 'Unknown')
        threads = result.get('threads', 'N/A')
        primes = result.get('primes_found', 'N/A')
        time_sec = result.get('time_seconds', 'N/A')
        
        # Calculate relative speed
        if isinstance(time_sec, (int, float)) and time_sec > 0:
            relative_speed = f"{fastest_time/time_sec:.2f}x"
            if i == 1:
                relative_speed = "1.00x (fastest)"
        else:
            relative_speed = "N/A"
        
        print(f"{language:<15} {str(threads):<10} {str(primes):<15} {time_sec:<12.6f} {relative_speed}")
    
    print("-"*80)
    print()

def print_statistics(results):
    """Print statistical analysis"""
    if not results:
        return
    
    times = [r.get('time_seconds') for r in results if 'time_seconds' in r]
    
    if not times:
        return
    
    print("\n" + "="*80)
    print("STATISTICAL ANALYSIS")
    print("="*80)
    print(f"Total languages tested: {len(results)}")
    print(f"Fastest time: {min(times):.6f} seconds")
    print(f"Slowest time: {max(times):.6f} seconds")
    print(f"Average time: {sum(times)/len(times):.6f} seconds")
    print(f"Speed difference (slowest/fastest): {max(times)/min(times):.2f}x")
    print()

def print_multithreading_analysis(results):
    """Analyze multithreading effectiveness"""
    print("\n" + "="*80)
    print("MULTITHREADING ANALYSIS")
    print("="*80)
    
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
    
    print("="*80)
    print("Analysis complete!")
    print("="*80)
    print()

if __name__ == "__main__":
    main()
