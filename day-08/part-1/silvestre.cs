using System;
using System.Collections.Generic;


namespace Aoc
{
    enum State {SignalPatterns, Digits};
    class Solution
    {
        private static void UpdateCounter(ref int counter, ref ushort currentLength){
            if (currentLength < 5) counter++;
            else if (currentLength > 6) counter++; 
        }
        private static int Solve(char[] input) {
            int counter = 0;
            ushort cursor = 0;
            ushort currentLength = 0;
            State state = State.SignalPatterns;
            while (cursor < input.Length) {
                switch (state, input[cursor]) {
                    case (State.SignalPatterns, '|'):
                        state = State.Digits;
                        currentLength=0;
                        cursor+=2;
                        break;
                    case (State.Digits, ' '):
                        UpdateCounter(ref counter, ref currentLength);
                        currentLength = 0;
                        cursor++;
                        break;
                    case (State.Digits, '\n'):
                        UpdateCounter(ref counter, ref currentLength);
                        state = State.SignalPatterns;
                        cursor++;
                        break;
                    default:
                        currentLength++;
                        cursor++;
                        break;
                }
            }
            UpdateCounter(ref counter, ref currentLength);
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
