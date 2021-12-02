using System;
using System.Collections.Generic;


namespace Aoc
{
    class Solution
    {
        private static string solve(string input) {
            int depth = 0;
            int horizontalPosition = 0;
            int offset;
            foreach(string line in input.Split('\n')){
                offset = line[line.Length-1] - '0';
                if(line[0] == 'f'){
                    horizontalPosition += offset;
                } else if(line[0] == 'u'){
                    depth -= offset;
                } else {
                    depth += offset;
                }
            }
            return Convert.ToString(depth * horizontalPosition);
        }

        public static void Main(string[] args) {
            string input = args[0];
            var watch = new System.Diagnostics.Stopwatch();
            watch.Start();
            string result = solve(input);
            watch.Stop();
            Console.WriteLine("_duration: " + watch.Elapsed.TotalMilliseconds + "\n" + result);
        }
        
    }
}
