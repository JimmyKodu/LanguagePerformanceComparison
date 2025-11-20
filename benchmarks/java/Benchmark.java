import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicLong;

class BenchmarkResult {
    String language;
    int threads;
    double duration_seconds;
    double actual_time_seconds;
    long primes_found;
    long primes_per_second;

    public BenchmarkResult(String language, int threads, double durationSeconds, double actualTimeSeconds, long primesFound, long primesPerSecond) {
        this.language = language;
        this.threads = threads;
        this.duration_seconds = durationSeconds;
        this.actual_time_seconds = actualTimeSeconds;
        this.primes_found = primesFound;
        this.primes_per_second = primesPerSecond;
    }

    public String toJson() {
        return String.format("{\n  \"language\": \"%s\",\n  \"threads\": %d,\n  \"duration_seconds\": %.1f,\n  \"actual_time_seconds\": %.6f,\n  \"primes_found\": %d,\n  \"primes_per_second\": %d\n}",
            language, threads, duration_seconds, actual_time_seconds, primes_found, primes_per_second);
    }
}

class PrimeCounter implements Callable<Long> {
    private final double duration;

    public PrimeCounter(double duration) {
        this.duration = duration;
    }

    private boolean isPrime(int n) {
        if (n < 2) return false;
        if (n == 2) return true;
        if (n % 2 == 0) return false;
        int sqrtN = (int) Math.sqrt(n);
        for (int i = 3; i <= sqrtN; i += 2) {
            if (n % i == 0) return false;
        }
        return true;
    }

    @Override
    public Long call() {
        long count = 0;
        int num = 2;
        long startTime = System.nanoTime();
        
        while (true) {
            if (isPrime(num)) {
                count++;
            }
            num++;
            
            // Check time periodically (every 1000 numbers to reduce overhead)
            if (num % 1000 == 0) {
                double elapsed = (System.nanoTime() - startTime) / 1_000_000_000.0;
                if (elapsed >= duration) {
                    break;
                }
            }
        }
        
        return count;
    }
}

public class Benchmark {
    public static BenchmarkResult runBenchmark(int numThreads, double duration) throws InterruptedException, ExecutionException {
        long startTime = System.nanoTime();

        ExecutorService executor = Executors.newFixedThreadPool(numThreads);
        Future<Long>[] futures = new Future[numThreads];

        for (int i = 0; i < numThreads; i++) {
            futures[i] = executor.submit(new PrimeCounter(duration));
        }

        long totalPrimes = 0;
        for (Future<Long> future : futures) {
            totalPrimes += future.get();
        }

        executor.shutdown();
        long endTime = System.nanoTime();
        double actualSeconds = (endTime - startTime) / 1_000_000_000.0;
        long primesPerSecond = (long)(totalPrimes / actualSeconds);

        return new BenchmarkResult("Java", numThreads, duration, actualSeconds, totalPrimes, primesPerSecond);
    }

    public static void main(String[] args) {
        int numThreads = args.length > 0 ? Integer.parseInt(args[0]) : 4;
        double duration = args.length > 1 ? Double.parseDouble(args[1]) : 1.0;

        try {
            BenchmarkResult result = runBenchmark(numThreads, duration);
            System.out.println(result.toJson());
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
