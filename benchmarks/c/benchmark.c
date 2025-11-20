#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <math.h>
#include <time.h>
#include <stdbool.h>
#include <stdatomic.h>

typedef struct {
    double duration;
    atomic_long* total_count;
} ThreadData;

bool is_prime(int n) {
    if (n < 2) return false;
    if (n == 2) return true;
    if (n % 2 == 0) return false;
    int sqrt_n = (int)sqrt(n);
    for (int i = 3; i <= sqrt_n; i += 2) {
        if (n % i == 0) return false;
    }
    return true;
}

void* count_primes_for_duration(void* arg) {
    ThreadData* data = (ThreadData*)arg;
    long count = 0;
    int num = 2;
    
    struct timespec start_time, current_time;
    clock_gettime(CLOCK_MONOTONIC, &start_time);
    
    while (1) {
        if (is_prime(num)) {
            count++;
        }
        num++;
        
        // Check time periodically (every 1000 numbers to reduce overhead)
        if (num % 1000 == 0) {
            clock_gettime(CLOCK_MONOTONIC, &current_time);
            double elapsed = (current_time.tv_sec - start_time.tv_sec) + 
                           (current_time.tv_nsec - start_time.tv_nsec) / 1e9;
            if (elapsed >= data->duration) {
                break;
            }
        }
    }
    
    atomic_fetch_add(data->total_count, count);
    return NULL;
}

int main(int argc, char* argv[]) {
    int num_threads = argc > 1 ? atoi(argv[1]) : 4;
    double duration = argc > 2 ? atof(argv[2]) : 1.0;

    struct timespec start_time, end_time;
    clock_gettime(CLOCK_MONOTONIC, &start_time);

    pthread_t* threads = malloc(num_threads * sizeof(pthread_t));
    ThreadData* thread_data = malloc(num_threads * sizeof(ThreadData));
    atomic_long total_primes = 0;

    for (int i = 0; i < num_threads; i++) {
        thread_data[i].duration = duration;
        thread_data[i].total_count = &total_primes;
        pthread_create(&threads[i], NULL, count_primes_for_duration, &thread_data[i]);
    }

    for (int i = 0; i < num_threads; i++) {
        pthread_join(threads[i], NULL);
    }

    clock_gettime(CLOCK_MONOTONIC, &end_time);
    double actual_time = (end_time.tv_sec - start_time.tv_sec) + 
                        (end_time.tv_nsec - start_time.tv_nsec) / 1e9;

    long primes = atomic_load(&total_primes);
    long primes_per_sec = (long)(primes / actual_time);

    printf("{\n");
    printf("  \"language\": \"C\",\n");
    printf("  \"threads\": %d,\n", num_threads);
    printf("  \"duration_seconds\": %.1f,\n", duration);
    printf("  \"actual_time_seconds\": %.6f,\n", actual_time);
    printf("  \"primes_found\": %ld,\n", primes);
    printf("  \"primes_per_second\": %ld\n", primes_per_sec);
    printf("}\n");

    free(threads);
    free(thread_data);

    return 0;
}
