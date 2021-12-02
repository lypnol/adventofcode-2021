<?php

const FWD = 'forward';
const DWN = 'down';
CONST UPW = 'up';

function run(string $input): int
{
    $depth = 0;
    $aim = 0;
    $horiz = 0;
    $lines = explode("\n", $input);

    foreach ($lines as $line) {
        $inst = explode(" ", $line);
        switch ($inst[0]) {
            case FWD:
                $x = (int) $inst[1];
                $horiz += $x;
                $depth += $aim * $x;
                break;
            case DWN:
                $aim += (int) $inst[1];
                break;
            case UPW:
                $aim -= (int) $inst[1];
                break;
        }
    }

    return $horiz * $depth;
}

$startTime = microtime(true);
$answer = run($argv[1]);
$endTime = microtime(true);

fwrite(STDOUT, sprintf("_duration:%f\n", ($endTime - $startTime)*1000));
fwrite(STDOUT, $answer."\n");
