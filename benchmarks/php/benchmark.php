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

function count_primes($max_number) {
    $count = 0;
    for ($num = 0; $num < $max_number; $num++) {
        if (is_prime($num)) {
            $count++;
        }
    }
    return $count;
}

function run_benchmark($max_number = 100000) {
    $start_time = microtime(true);
    
    $total_primes = count_primes($max_number);
    
    $end_time = microtime(true);
    $elapsed = $end_time - $start_time;
    
    return [
        'language' => 'PHP',
        'threads' => 1,  // PHP is single-threaded
        'max_number' => $max_number,
        'primes_found' => $total_primes,
        'time_seconds' => $elapsed
    ];
}

// Main execution
$max_number = isset($argv[2]) ? (int)$argv[2] : 100000;

$result = run_benchmark($max_number);
echo json_encode($result, JSON_PRETTY_PRINT) . "\n";
?>
