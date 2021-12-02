<?php

function run(string $input): int
{
    $lines = explode("\n", $input);
    $count = 0;
    $prev = (int) $lines[0];
    foreach ($lines as $line) {
        $curr = (int) $line;
        if ($prev < $curr) {
            $count++;
        }
        $prev = $curr;
    }

    return $count;
}

$startTime = microtime(true);
$answer = run($argv[1]);
$endTime = microtime(true);

fwrite(STDOUT, sprintf("_duration:%f\n", ($endTime - $startTime)*1000));
fwrite(STDOUT, $answer."\n");
