#include <iostream>
#include <thread>
#include <vector>
#include <cmath>
#include <chrono>
#include <string>
#include <sstream>

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

void count_primes_in_range(int start, int end, int& result) {
    int count = 0;
    for (int num = start; num < end; num++) {
        if (is_prime(num)) {
            count++;
        }
    }
    result = count;
}

int main(int argc, char* argv[]) {
    int num_threads = argc > 1 ? std::stoi(argv[1]) : 4;
    int max_number = argc > 2 ? std::stoi(argv[2]) : 100000;

    auto start_time = std::chrono::high_resolution_clock::now();

    std::vector<std::thread> threads;
    std::vector<int> results(num_threads, 0);
    int chunk_size = max_number / num_threads;

    for (int i = 0; i < num_threads; i++) {
        int start = i * chunk_size;
        int end = (i == num_threads - 1) ? max_number : (i + 1) * chunk_size;
        threads.emplace_back(count_primes_in_range, start, end, std::ref(results[i]));
    }

    for (auto& thread : threads) {
        thread.join();
    }

    int total_primes = 0;
    for (int count : results) {
        total_primes += count;
    }

    auto end_time = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = end_time - start_time;

    std::cout << "{\n";
    std::cout << "  \"language\": \"C++\",\n";
    std::cout << "  \"threads\": " << num_threads << ",\n";
    std::cout << "  \"max_number\": " << max_number << ",\n";
    std::cout << "  \"primes_found\": " << total_primes << ",\n";
    std::cout << "  \"time_seconds\": " << elapsed.count() << "\n";
    std::cout << "}\n";

    return 0;
}
