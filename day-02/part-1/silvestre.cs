using System;
using System.Collections.Generic;


namespace Aoc
{
    class Solution
    {
        private static int solve(char[] input) {
            int depth = 0;
            int position = 0;
            int offset;
            char direction = input[0];
            int cursor = 0;
            while (cursor < input.Length) {
                switch (input[cursor]) {
                    case 'f':
                        position += (int)(input[cursor+8] - '0');
                        cursor += 10;
                        break;
                    case 'u':
                        depth -= (int)(input[cursor+3] - '0');
                        cursor += 5;
                        break;
                    case 'd':
                        depth += (int)(input[cursor+5] - '0');
                        cursor += 7;
                        break;
                }
            }
            return depth * position;
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
