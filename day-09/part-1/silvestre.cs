using System;
using System.Collections.Generic;


namespace Aoc
{
    class Solution
    {
        private const ushort LINE_LENGTH = 100+1;
        private const ushort N_LINES = 100;
        private static int Solve(char[] input) {
            int counter = 0;
            ushort cursor = 0;
            ushort col = 1;
            while (cursor < LINE_LENGTH * N_LINES - 1) {
                if (input[cursor] == '\n') {col = 0;}
                else if (
                    ((cursor < LINE_LENGTH) || (input[cursor] < input[cursor-LINE_LENGTH])) &&
                    ((cursor >= LINE_LENGTH * (N_LINES-1)) || (input[cursor] < input[cursor+LINE_LENGTH])) &&
                    ((col == 1) || (input[cursor] < input[cursor-1])) &&
                    ((col == LINE_LENGTH-1) || (input[cursor] < input[cursor+1]))
                ) {
                    counter+= (int)(input[cursor] - '0' + 1);
                }
                ++col;
                ++cursor;
            }
            return counter;
        }

        public static void Main(string[] args) {
            char[] input = args[0].ToCharArray();
            var watch = new System.Diagnostics.Stopwatch();
            watch.Start();
            int result = Solve(input);
            watch.Stop();
            Console.WriteLine("_duration: " + watch.Elapsed.TotalMilliseconds + "\n" + result);
        }
        
    }
}
