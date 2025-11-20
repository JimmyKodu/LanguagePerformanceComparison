package main

import (
	"encoding/json"
	"fmt"
	"math"
	"os"
	"strconv"
	"sync"
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

// countPrimesInRange counts prime numbers in a given range
func countPrimesInRange(start, end int, wg *sync.WaitGroup, results chan int) {
	defer wg.Done()
	count := 0
	for num := start; num < end; num++ {
		if isPrime(num) {
			count++
		}
	}
	results <- count
}

// BenchmarkResult represents the benchmark output
type BenchmarkResult struct {
	Language    string  `json:"language"`
	Threads     int     `json:"threads"`
	MaxNumber   int     `json:"max_number"`
	PrimesFound int     `json:"primes_found"`
	TimeSeconds float64 `json:"time_seconds"`
}

func benchmark(numThreads, maxNumber int) BenchmarkResult {
	startTime := time.Now()

	// Divide work among goroutines
	chunkSize := maxNumber / numThreads
	results := make(chan int, numThreads)
	var wg sync.WaitGroup

	for i := 0; i < numThreads; i++ {
		start := i * chunkSize
		end := (i + 1) * chunkSize
		if i == numThreads-1 {
			end = maxNumber
		}

		wg.Add(1)
		go countPrimesInRange(start, end, &wg, results)
	}

	// Wait for all goroutines to complete
	wg.Wait()
	close(results)

	// Sum up results
	totalPrimes := 0
	for count := range results {
		totalPrimes += count
	}

	elapsed := time.Since(startTime).Seconds()

	return BenchmarkResult{
		Language:    "Go",
		Threads:     numThreads,
		MaxNumber:   maxNumber,
		PrimesFound: totalPrimes,
		TimeSeconds: elapsed,
	}
}

func main() {
	numThreads := 4
	maxNumber := 100000

	if len(os.Args) > 1 {
		numThreads, _ = strconv.Atoi(os.Args[1])
	}
	if len(os.Args) > 2 {
		maxNumber, _ = strconv.Atoi(os.Args[2])
	}

	result := benchmark(numThreads, maxNumber)
	jsonOutput, _ := json.MarshalIndent(result, "", "  ")
	fmt.Println(string(jsonOutput))
}
