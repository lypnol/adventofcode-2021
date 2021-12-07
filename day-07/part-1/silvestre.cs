using System;
using System.Collections.Generic;


namespace Aoc
{
    class Solution
    {
        private static (int[], int) Parse(char[] input) {
            int[] result = new int[1000];
            int size = 0;
            ushort cursor = 0;
            int num_acc = 0;
            while (cursor < input.Length) {
                switch (input[cursor]) {
                    case ',':
                        result[size] = num_acc;
                        num_acc = 0;
                        size++;
                        cursor++;
                        break;
                    default:
                        num_acc = num_acc * 10 + (int)(input[cursor] - '0');
                        cursor++;
                        break;
                }
            }
            result[size] = num_acc;
            size++;
            return (result, size);
        }
        private static int Solve(char[] input) {
            (int[] positions, int size) = Parse(input);
            Array.Sort(positions, 0, size);
            int median = positions[(int) (size / 2)];
            int result = 0;
            for (int idx=0; idx<size; idx++) {
                result += positions[idx] > median ? positions[idx] - median : median - positions[idx];
            }
            return result;
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
