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
            int gamma = 0;
            int colCount = 0;
            int offset = 1;
            for (int colIndex=LINE_LENGHT-1;colIndex>-1;colIndex--){
                colCount = 0;
                for (int cursor=colIndex;cursor<input.Length;cursor+=LINE_LENGHT+1) {
                    colCount += (int)(input[cursor] - '0');
                }
                if (2 * colCount > N_LINES) { gamma |= offset;}
                offset <<= 1;
            }
            int epsilon = ((1 << LINE_LENGHT)-1) ^ gamma;
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
