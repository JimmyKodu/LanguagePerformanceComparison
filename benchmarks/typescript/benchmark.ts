import { Worker } from 'worker_threads';
import * as path from 'path';

interface BenchmarkResult {
    language: string;
    threads: number;
    duration_seconds: number;
    actual_time_seconds: number;
    primes_found: number;
    primes_per_second: number;
}

function runWorker(duration: number): Promise<number> {
    return new Promise((resolve, reject) => {
        const worker = new Worker(path.join(__dirname, 'worker.js'), {
            workerData: { duration }
        });
        worker.on('message', resolve);
        worker.on('error', reject);
        worker.on('exit', (code) => {
            if (code !== 0) {
                reject(new Error(`Worker stopped with exit code ${code}`));
            }
        });
    });
}

async function benchmark(numThreads: number = 4, duration: number = 1.0): Promise<BenchmarkResult> {
    const startTime = Date.now();
    
    const promises: Promise<number>[] = [];
    
    for (let i = 0; i < numThreads; i++) {
        promises.push(runWorker(duration));
    }
    
    const results = await Promise.all(promises);
    const totalPrimes = results.reduce((sum, count) => sum + count, 0);
    
    const endTime = Date.now();
    const actualSeconds = (endTime - startTime) / 1000;
    const primesPerSecond = Math.floor(totalPrimes / actualSeconds);
    
    return {
        language: 'TypeScript',
        threads: numThreads,
        duration_seconds: duration,
        actual_time_seconds: actualSeconds,
        primes_found: totalPrimes,
        primes_per_second: primesPerSecond
    };
}

// Main execution
const numThreads = process.argv[2] ? parseInt(process.argv[2]) : 4;
const duration = process.argv[3] ? parseFloat(process.argv[3]) : 1.0;

benchmark(numThreads, duration).then(result => {
    console.log(JSON.stringify(result, null, 2));
}).catch(err => {
    console.error('Error:', err);
    process.exit(1);
});
