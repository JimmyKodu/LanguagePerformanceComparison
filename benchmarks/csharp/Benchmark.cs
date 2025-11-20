using System;
using System.Threading.Tasks;
using System.Diagnostics;
using System.Text.Json;

class BenchmarkResult
{
    public string language { get; set; }
    public int threads { get; set; }
    public int max_number { get; set; }
    public int primes_found { get; set; }
    public double time_seconds { get; set; }
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

    static int CountPrimesInRange(int start, int end)
    {
        int count = 0;
        for (int num = start; num < end; num++)
        {
            if (IsPrime(num))
            {
                count++;
            }
        }
        return count;
    }

    static BenchmarkResult RunBenchmark(int numThreads, int maxNumber)
    {
        var stopwatch = Stopwatch.StartNew();

        int chunkSize = maxNumber / numThreads;
        Task<int>[] tasks = new Task<int>[numThreads];

        for (int i = 0; i < numThreads; i++)
        {
            int start = i * chunkSize;
            int end = (i == numThreads - 1) ? maxNumber : (i + 1) * chunkSize;
            int threadIndex = i;
            tasks[i] = Task.Run(() => CountPrimesInRange(start, end));
        }

        Task.WaitAll(tasks);

        int totalPrimes = 0;
        foreach (var task in tasks)
        {
            totalPrimes += task.Result;
        }

        stopwatch.Stop();
        double elapsedSeconds = stopwatch.Elapsed.TotalSeconds;

        return new BenchmarkResult
        {
            language = "C#",
            threads = numThreads,
            max_number = maxNumber,
            primes_found = totalPrimes,
            time_seconds = elapsedSeconds
        };
    }

    static void Main(string[] args)
    {
        int numThreads = args.Length > 0 ? int.Parse(args[0]) : 4;
        int maxNumber = args.Length > 1 ? int.Parse(args[1]) : 100000;

        var result = RunBenchmark(numThreads, maxNumber);
        var options = new JsonSerializerOptions { WriteIndented = true };
        string jsonString = JsonSerializer.Serialize(result, options);
        Console.WriteLine(jsonString);
    }
}
