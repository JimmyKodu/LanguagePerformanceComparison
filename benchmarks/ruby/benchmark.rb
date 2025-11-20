#!/usr/bin/env ruby
# Ruby multithreading benchmark

require 'json'

def is_prime(n)
  return false if n < 2
  return true if n == 2
  return false if n.even?
  sqrt_n = Math.sqrt(n).to_i
  (3..sqrt_n).step(2) do |i|
    return false if n % i == 0
  end
  true
end

def count_primes_in_range(start, finish)
  count = 0
  (start...finish).each do |num|
    count += 1 if is_prime(num)
  end
  count
end

def benchmark(num_threads = 4, max_number = 100000)
  start_time = Time.now
  
  chunk_size = max_number / num_threads
  threads = []
  results = Array.new(num_threads, 0)
  
  num_threads.times do |i|
    start = i * chunk_size
    finish = (i == num_threads - 1) ? max_number : (i + 1) * chunk_size
    
    threads << Thread.new do
      results[i] = count_primes_in_range(start, finish)
    end
  end
  
  threads.each(&:join)
  
  total_primes = results.sum
  end_time = Time.now
  elapsed_time = end_time - start_time
  
  {
    language: 'Ruby',
    threads: num_threads,
    max_number: max_number,
    primes_found: total_primes,
    time_seconds: elapsed_time
  }
end

# Main execution
num_threads = ARGV[0] ? ARGV[0].to_i : 4
max_number = ARGV[1] ? ARGV[1].to_i : 100000

result = benchmark(num_threads, max_number)
puts JSON.pretty_generate(result)
