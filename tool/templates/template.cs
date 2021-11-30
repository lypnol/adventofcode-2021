using System;
using System.Collections.Generic;


namespace Aoc
{
    class Solution
    {
        private static string solve(string input) {
            // Your code goes here
            return "Nothing";
        }

        public static void Main(string[] args) {
            string input = args[0];
            var watch = new System.Diagnostics.Stopwatch();
            watch.Start();
            string result = solve(input);
            watch.Stop();
            Console.WriteLine("_duration: " + watch.ElapsedMilliseconds + "\n" + result);
        }
        
    }
}
