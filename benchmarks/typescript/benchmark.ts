import { Worker } from 'worker_threads';
import * as path from 'path';

interface BenchmarkResult {
    language: string;
    threads: number;
    max_number: number;
    primes_found: number;
    time_seconds: number;
}

function runWorker(start: number, end: number): Promise<number> {
    return new Promise((resolve, reject) => {
        const worker = new Worker(path.join(__dirname, 'worker.js'), {
            workerData: { start, end }
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

async function benchmark(numThreads: number = 4, maxNumber: number = 100000): Promise<BenchmarkResult> {
    const startTime = Date.now();
    
    const chunkSize = Math.floor(maxNumber / numThreads);
    const promises: Promise<number>[] = [];
    
    for (let i = 0; i < numThreads; i++) {
        const start = i * chunkSize;
        const end = (i === numThreads - 1) ? maxNumber : (i + 1) * chunkSize;
        promises.push(runWorker(start, end));
    }
    
    const results = await Promise.all(promises);
    const totalPrimes = results.reduce((sum, count) => sum + count, 0);
    
    const endTime = Date.now();
    const elapsedSeconds = (endTime - startTime) / 1000;
    
    return {
        language: 'TypeScript',
        threads: numThreads,
        max_number: maxNumber,
        primes_found: totalPrimes,
        time_seconds: elapsedSeconds
    };
}

// Main execution
const numThreads = process.argv[2] ? parseInt(process.argv[2]) : 4;
const maxNumber = process.argv[3] ? parseInt(process.argv[3]) : 100000;

benchmark(numThreads, maxNumber).then(result => {
    console.log(JSON.stringify(result, null, 2));
}).catch(err => {
    console.error('Error:', err);
    process.exit(1);
});
