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

def count_primes_for_duration(duration)
  count = 0
  num = 2
  start_time = Time.now
  
  loop do
    count += 1 if is_prime(num)
    num += 1
    
    # Check time periodically (every 1000 numbers to reduce overhead)
    if num % 1000 == 0
      break if Time.now - start_time >= duration
    end
  end
  
  count
end

def benchmark(num_threads = 4, duration = 1.0)
  start_time = Time.now
  
  threads = []
  results = Array.new(num_threads, 0)
  
  num_threads.times do |i|
    threads << Thread.new do
      results[i] = count_primes_for_duration(duration)
    end
  end
  
  threads.each(&:join)
  
  total_primes = results.sum
  actual_time = Time.now - start_time
  primes_per_sec = (total_primes / actual_time).to_i
  
  {
    language: 'Ruby',
    threads: num_threads,
    duration_seconds: duration,
    actual_time_seconds: actual_time,
    primes_found: total_primes,
    primes_per_second: primes_per_sec
  }
end

# Main execution
num_threads = ARGV[0] ? ARGV[0].to_i : 4
duration = ARGV[1] ? ARGV[1].to_f : 1.0

result = benchmark(num_threads, duration)
puts JSON.pretty_generate(result)
