const { parentPort, workerData } = require('worker_threads');

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

function countPrimesForDuration(duration) {
    let count = 0;
    let num = 2;
    const startTime = Date.now();
    
    while (true) {
        if (isPrime(num)) {
            count++;
        }
        num++;
        
        // Check time periodically (every 1000 numbers to reduce overhead)
        if (num % 1000 === 0) {
            if ((Date.now() - startTime) / 1000 >= duration) {
                break;
            }
        }
    }
    
    return count;
}

const { duration } = workerData;
const count = countPrimesForDuration(duration);
parentPort.postMessage(count);
