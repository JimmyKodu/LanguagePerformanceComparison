const { Worker } = require('worker_threads');
const path = require('path');

function isPrime(n) {
    if (n < 2) return false;
    if (n === 2) return true;
    if (n % 2 === 0) return false;
    const sqrtN = Math.floor(Math.sqrt(n));
    for (let i = 3; i <= sqrtN; i += 2) {
        if (n % i === 0) return false;
    }
    return true;
}

function countPrimesInRange(start, end) {
    let count = 0;
    for (let num = start; num < end; num++) {
        if (isPrime(num)) {
            count++;
        }
    }
    return count;
}

function runWorker(start, end) {
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

async function benchmark(numThreads = 4, maxNumber = 100000) {
    const startTime = Date.now();
    
    const chunkSize = Math.floor(maxNumber / numThreads);
    const promises = [];
    
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
        language: 'JavaScript',
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
