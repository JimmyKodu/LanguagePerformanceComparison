#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <math.h>
#include <time.h>
#include <stdbool.h>

typedef struct {
    int start;
    int end;
    int count;
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

void* count_primes_in_range(void* arg) {
    ThreadData* data = (ThreadData*)arg;
    data->count = 0;
    for (int num = data->start; num < data->end; num++) {
        if (is_prime(num)) {
            data->count++;
        }
    }
    return NULL;
}

int main(int argc, char* argv[]) {
    int num_threads = argc > 1 ? atoi(argv[1]) : 4;
    int max_number = argc > 2 ? atoi(argv[2]) : 100000;

    struct timespec start_time, end_time;
    clock_gettime(CLOCK_MONOTONIC, &start_time);

    pthread_t* threads = malloc(num_threads * sizeof(pthread_t));
    ThreadData* thread_data = malloc(num_threads * sizeof(ThreadData));

    int chunk_size = max_number / num_threads;

    for (int i = 0; i < num_threads; i++) {
        thread_data[i].start = i * chunk_size;
        thread_data[i].end = (i == num_threads - 1) ? max_number : (i + 1) * chunk_size;
        pthread_create(&threads[i], NULL, count_primes_in_range, &thread_data[i]);
    }

    int total_primes = 0;
    for (int i = 0; i < num_threads; i++) {
        pthread_join(threads[i], NULL);
        total_primes += thread_data[i].count;
    }

    clock_gettime(CLOCK_MONOTONIC, &end_time);
    double elapsed = (end_time.tv_sec - start_time.tv_sec) + 
                     (end_time.tv_nsec - start_time.tv_nsec) / 1e9;

    printf("{\n");
    printf("  \"language\": \"C\",\n");
    printf("  \"threads\": %d,\n", num_threads);
    printf("  \"max_number\": %d,\n", max_number);
    printf("  \"primes_found\": %d,\n", total_primes);
    printf("  \"time_seconds\": %.6f\n", elapsed);
    printf("}\n");

    free(threads);
    free(thread_data);

    return 0;
}
