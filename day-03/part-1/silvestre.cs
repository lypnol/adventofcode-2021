using System;
using System.Collections;
using System.Collections.Generic;


namespace Aoc
{
    class Solution
    {
        private static int LINE_LENGHT = 12;
        private static int N_LINES = 1000;

        private static int solve(char[] input) {
            int[] bitCounts = new int[LINE_LENGHT];
            int colIndex = 0;
            for (int index = 0; index < input.Length; index++){
                if (input[index] == '\n'){
                    colIndex = 0;
                } else {
                    bitCounts[colIndex] += (int)(input[index]- '0');
                    colIndex++;
                }
            }
            int gamma = 0;
            int epsilon = 0;
            for (int idx = 0;idx<LINE_LENGHT;idx++) {
                if (2 * bitCounts[idx] > N_LINES) {
                    gamma += 1 << (LINE_LENGHT - idx - 1);
                }
                else {epsilon += 1 << (LINE_LENGHT - idx - 1);}
            }
            return gamma * epsilon;
        }

        public static void Main(string[] args) {
            char[] input = args[0].ToCharArray();
            var watch = new System.Diagnostics.Stopwatch();
            watch.Start();
            int result = solve(input);
            watch.Stop();
            Console.WriteLine("_duration: " + watch.Elapsed.TotalMilliseconds + "\n" + result);
        }
        
    }
}
