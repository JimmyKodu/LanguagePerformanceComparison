#include <iostream>
#include <thread>
#include <vector>
#include <cmath>
#include <chrono>
#include <atomic>

bool is_prime(int n) {
    if (n < 2) return false;
    if (n == 2) return true;
    if (n % 2 == 0) return false;
    int sqrt_n = static_cast<int>(std::sqrt(n));
    for (int i = 3; i <= sqrt_n; i += 2) {
        if (n % i == 0) return false;
    }
    return true;
}

void count_primes_for_duration(double duration, std::atomic<long>& total_count) {
    long count = 0;
    int num = 2;
    auto start_time = std::chrono::high_resolution_clock::now();
    
    while (true) {
        if (is_prime(num)) {
            count++;
        }
        num++;
        
        // Check time periodically (every 1000 numbers to reduce overhead)
        if (num % 1000 == 0) {
            auto current_time = std::chrono::high_resolution_clock::now();
            std::chrono::duration<double> elapsed = current_time - start_time;
            if (elapsed.count() >= duration) {
                break;
            }
        }
    }
    
    total_count += count;
}

int main(int argc, char* argv[]) {
    int num_threads = argc > 1 ? std::stoi(argv[1]) : 4;
    double duration = argc > 2 ? std::stod(argv[2]) : 1.0;

    auto start_time = std::chrono::high_resolution_clock::now();

    std::vector<std::thread> threads;
    std::atomic<long> total_primes(0);

    for (int i = 0; i < num_threads; i++) {
        threads.emplace_back(count_primes_for_duration, duration, std::ref(total_primes));
    }

    for (auto& thread : threads) {
        thread.join();
    }

    auto end_time = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> actual_time = end_time - start_time;

    long primes = total_primes.load();
    long primes_per_sec = static_cast<long>(primes / actual_time.count());

    std::cout << "{\n";
    std::cout << "  \"language\": \"C++\",\n";
    std::cout << "  \"threads\": " << num_threads << ",\n";
    std::cout << "  \"duration_seconds\": " << duration << ",\n";
    std::cout << "  \"actual_time_seconds\": " << actual_time.count() << ",\n";
    std::cout << "  \"primes_found\": " << primes << ",\n";
    std::cout << "  \"primes_per_second\": " << primes_per_sec << "\n";
    std::cout << "}\n";

    return 0;
}
