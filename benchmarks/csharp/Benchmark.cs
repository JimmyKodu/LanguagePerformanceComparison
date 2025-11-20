using System;
using System.Threading.Tasks;
using System.Diagnostics;
using System.Text.Json;
using System.Threading;

class BenchmarkResult
{
    public string language { get; set; }
    public int threads { get; set; }
    public double duration_seconds { get; set; }
    public double actual_time_seconds { get; set; }
    public long primes_found { get; set; }
    public long primes_per_second { get; set; }
}

class Program
{
    static bool IsPrime(int n)
    {
        if (n < 2) return false;
        if (n == 2) return true;
        if (n % 2 == 0) return false;
        int sqrtN = (int)Math.Sqrt(n);
        for (int i = 3; i <= sqrtN; i += 2)
        {
            if (n % i == 0) return false;
        }
        return true;
    }

    static long CountPrimesForDuration(double duration)
    {
        long count = 0;
        int num = 2;
        var stopwatch = Stopwatch.StartNew();

        while (true)
        {
            if (IsPrime(num))
            {
                count++;
            }
            num++;

            // Check time periodically (every 1000 numbers to reduce overhead)
            if (num % 1000 == 0)
            {
                if (stopwatch.Elapsed.TotalSeconds >= duration)
                {
                    break;
                }
            }
        }

        return count;
    }

    static BenchmarkResult RunBenchmark(int numThreads, double duration)
    {
        var stopwatch = Stopwatch.StartNew();

        Task<long>[] tasks = new Task<long>[numThreads];

        for (int i = 0; i < numThreads; i++)
        {
            tasks[i] = Task.Run(() => CountPrimesForDuration(duration));
        }

        Task.WaitAll(tasks);

        long totalPrimes = 0;
        foreach (var task in tasks)
        {
            totalPrimes += task.Result;
        }

        stopwatch.Stop();
        double actualSeconds = stopwatch.Elapsed.TotalSeconds;
        long primesPerSecond = (long)(totalPrimes / actualSeconds);

        return new BenchmarkResult
        {
            language = "C#",
            threads = numThreads,
            duration_seconds = duration,
            actual_time_seconds = actualSeconds,
            primes_found = totalPrimes,
            primes_per_second = primesPerSecond
        };
    }

    static void Main(string[] args)
    {
        int numThreads = args.Length > 0 ? int.Parse(args[0]) : 4;
        double duration = args.Length > 1 ? double.Parse(args[1]) : 1.0;

        var result = RunBenchmark(numThreads, duration);
        var options = new JsonSerializerOptions { WriteIndented = true };
        string jsonString = JsonSerializer.Serialize(result, options);
        Console.WriteLine(jsonString);
    }
}
