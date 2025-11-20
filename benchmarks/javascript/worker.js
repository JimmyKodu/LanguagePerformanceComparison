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

function countPrimesInRange(start, end) {
    let count = 0;
    for (let num = start; num < end; num++) {
        if (isPrime(num)) {
            count++;
        }
    }
    return count;
}

const { start, end } = workerData;
const count = countPrimesInRange(start, end);
parentPort.postMessage(count);
