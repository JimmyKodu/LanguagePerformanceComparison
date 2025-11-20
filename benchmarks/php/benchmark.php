<?php
/**
 * PHP benchmark - single-threaded
 * PHP doesn't have native multithreading support in standard installations
 */

function is_prime($n) {
    if ($n < 2) return false;
    if ($n == 2) return true;
    if ($n % 2 == 0) return false;
    $sqrt_n = (int)sqrt($n);
    for ($i = 3; $i <= $sqrt_n; $i += 2) {
        if ($n % $i == 0) return false;
    }
    return true;
}

function count_primes_for_duration($duration) {
    $count = 0;
    $num = 2;
    $start_time = microtime(true);
    
    while (true) {
        if (is_prime($num)) {
            $count++;
        }
        $num++;
        
        // Check time periodically (every 1000 numbers to reduce overhead)
        if ($num % 1000 == 0) {
            if (microtime(true) - $start_time >= $duration) {
                break;
            }
        }
    }
    
    return $count;
}

function run_benchmark($duration = 1.0) {
    $start_time = microtime(true);
    
    $total_primes = count_primes_for_duration($duration);
    
    $actual_time = microtime(true) - $start_time;
    $primes_per_sec = (int)($total_primes / $actual_time);
    
    return [
        'language' => 'PHP',
        'threads' => 1,  // PHP is single-threaded
        'duration_seconds' => $duration,
        'actual_time_seconds' => $actual_time,
        'primes_found' => $total_primes,
        'primes_per_second' => $primes_per_sec
    ];
}

// Main execution
$duration = isset($argv[2]) ? (float)$argv[2] : 1.0;

$result = run_benchmark($duration);
echo json_encode($result, JSON_PRETTY_PRINT) . "\n";
?>
