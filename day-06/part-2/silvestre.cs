using System;
using System.Collections.Generic;


namespace Aoc
{
    class Solution
    {
        private static ulong Solve(char[] input) {
            ulong[] fishs = new ulong[9];
            ushort index = 0;
            while (index < input.Length) {
                fishs[(int)(input[index] - '0')]++;
                index += 2;
            }
            ulong newFishs = 0;
            for (ushort day=1; day<=256; day++) {
                newFishs = fishs[0];
                for (ushort idx=0;idx<8;idx++){
                    fishs[idx] = fishs[idx+1];
                }
                fishs[6] += newFishs;
                fishs[8] = newFishs;
            }
            ulong total = 0;
            for (ushort idx=0;idx<fishs.Length;idx++){total+=fishs[idx];}
            return total;
        }

        public static void Main(string[] args) {
            char[] input = args[0].ToCharArray();
            var watch = new System.Diagnostics.Stopwatch();
            watch.Start();
            ulong result = Solve(input);
            watch.Stop();
            Console.WriteLine("_duration: " + watch.Elapsed.TotalMilliseconds + "\n" + result);
        }
        
    }
}
