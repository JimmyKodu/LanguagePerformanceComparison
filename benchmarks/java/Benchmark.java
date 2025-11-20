import java.util.concurrent.*;

class BenchmarkResult {
    String language;
    int threads;
    int max_number;
    int primes_found;
    double time_seconds;

    public BenchmarkResult(String language, int threads, int maxNumber, int primesFound, double timeSeconds) {
        this.language = language;
        this.threads = threads;
        this.max_number = maxNumber;
        this.primes_found = primesFound;
        this.time_seconds = timeSeconds;
    }

    public String toJson() {
        return String.format("{\n  \"language\": \"%s\",\n  \"threads\": %d,\n  \"max_number\": %d,\n  \"primes_found\": %d,\n  \"time_seconds\": %.6f\n}",
            language, threads, max_number, primes_found, time_seconds);
    }
}

class PrimeCounter implements Callable<Integer> {
    private final int start;
    private final int end;

    public PrimeCounter(int start, int end) {
        this.start = start;
        this.end = end;
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
    public Integer call() {
        int count = 0;
        for (int num = start; num < end; num++) {
            if (isPrime(num)) {
                count++;
            }
        }
        return count;
    }
}

public class Benchmark {
    public static BenchmarkResult runBenchmark(int numThreads, int maxNumber) throws InterruptedException, ExecutionException {
        long startTime = System.nanoTime();

        ExecutorService executor = Executors.newFixedThreadPool(numThreads);
        int chunkSize = maxNumber / numThreads;
        Future<Integer>[] futures = new Future[numThreads];

        for (int i = 0; i < numThreads; i++) {
            int start = i * chunkSize;
            int end = (i == numThreads - 1) ? maxNumber : (i + 1) * chunkSize;
            futures[i] = executor.submit(new PrimeCounter(start, end));
        }

        int totalPrimes = 0;
        for (Future<Integer> future : futures) {
            totalPrimes += future.get();
        }

        executor.shutdown();
        long endTime = System.nanoTime();
        double elapsedSeconds = (endTime - startTime) / 1_000_000_000.0;

        return new BenchmarkResult("Java", numThreads, maxNumber, totalPrimes, elapsedSeconds);
    }

    public static void main(String[] args) {
        int numThreads = args.length > 0 ? Integer.parseInt(args[0]) : 4;
        int maxNumber = args.length > 1 ? Integer.parseInt(args[1]) : 100000;

        try {
            BenchmarkResult result = runBenchmark(numThreads, maxNumber);
            System.out.println(result.toJson());
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
