using System;
using System.Collections.Generic;


namespace Aoc
{
    class Solution
    {
        private static uint Solve(char[] input) {
            uint[] fishs = new uint[9];
            ushort index = 0;
            while (index < input.Length) {
                fishs[(int)(input[index] - '0')]++;
                index += 2;
            }
            uint newFishs = 0;
            for (ushort day=1; day<=80; day++) {
                newFishs = fishs[0];
                for (ushort idx=0;idx<8;idx++){
                    fishs[idx] = fishs[idx+1];
                }
                fishs[6] += newFishs;
                fishs[8] = newFishs;
            }
            uint total = 0;
            for (ushort idx=0;idx<fishs.Length;idx++){total+=fishs[idx];}
            return total;
        }

        public static void Main(string[] args) {
            char[] input = args[0].ToCharArray();
            var watch = new System.Diagnostics.Stopwatch();
            watch.Start();
            uint result = Solve(input);
            watch.Stop();
            Console.WriteLine("_duration: " + watch.Elapsed.TotalMilliseconds + "\n" + result);
        }
        
    }
}
