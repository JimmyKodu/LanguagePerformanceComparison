package main

import (
	"encoding/json"
	"fmt"
	"math"
	"os"
	"strconv"
	"sync"
	"sync/atomic"
	"time"
)

// isPrime checks if a number is prime
func isPrime(n int) bool {
	if n < 2 {
		return false
	}
	if n == 2 {
		return true
	}
	if n%2 == 0 {
		return false
	}
	sqrtN := int(math.Sqrt(float64(n)))
	for i := 3; i <= sqrtN; i += 2 {
		if n%i == 0 {
			return false
		}
	}
	return true
}

// countPrimesForDuration counts prime numbers for a given duration
func countPrimesForDuration(duration time.Duration, wg *sync.WaitGroup, result *int64) {
	defer wg.Done()
	count := int64(0)
	num := 2
	startTime := time.Now()

	for {
		if isPrime(num) {
			count++
		}
		num++

		// Check time periodically (every 1000 numbers to reduce overhead)
		if num%1000 == 0 {
			if time.Since(startTime) >= duration {
				break
			}
		}
	}

	atomic.AddInt64(result, count)
}

// BenchmarkResult represents the benchmark output
type BenchmarkResult struct {
	Language         string  `json:"language"`
	Threads          int     `json:"threads"`
	DurationSeconds  float64 `json:"duration_seconds"`
	ActualTimeSeconds float64 `json:"actual_time_seconds"`
	PrimesFound      int64   `json:"primes_found"`
	PrimesPerSecond  int64   `json:"primes_per_second"`
}

func benchmark(numThreads int, duration float64) BenchmarkResult {
	startTime := time.Now()
	durationTime := time.Duration(duration * float64(time.Second))

	var totalPrimes int64
	var wg sync.WaitGroup

	for i := 0; i < numThreads; i++ {
		wg.Add(1)
		go countPrimesForDuration(durationTime, &wg, &totalPrimes)
	}

	// Wait for all goroutines to complete
	wg.Wait()

	actualTime := time.Since(startTime).Seconds()
	primesPerSecond := int64(float64(totalPrimes) / actualTime)

	return BenchmarkResult{
		Language:         "Go",
		Threads:          numThreads,
		DurationSeconds:  duration,
		ActualTimeSeconds: actualTime,
		PrimesFound:      totalPrimes,
		PrimesPerSecond:  primesPerSecond,
	}
}

func main() {
	numThreads := 4
	duration := 1.0

	if len(os.Args) > 1 {
		numThreads, _ = strconv.Atoi(os.Args[1])
	}
	if len(os.Args) > 2 {
		duration, _ = strconv.ParseFloat(os.Args[2], 64)
	}

	result := benchmark(numThreads, duration)
	jsonOutput, _ := json.MarshalIndent(result, "", "  ")
	fmt.Println(string(jsonOutput))
}
