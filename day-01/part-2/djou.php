<?php

function run(string $input): int
{
    $lines = explode("\n", $input);
    $count = 0;
    for ($i = 3; $i < count($lines); $i++) {
        if ((int) $lines[$i - 3] < (int) $lines[$i]) {
            $count++;
        }
    }

    return $count;
}

$startTime = microtime(true);
$answer = run($argv[1]);
$endTime = microtime(true);

fwrite(STDOUT, sprintf("_duration:%f\n", ($endTime - $startTime)*1000));
fwrite(STDOUT, $answer."\n");
