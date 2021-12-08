using System;
using System.Collections.Generic;


namespace Aoc
{
    enum State {SignalPatterns, Digits};
    class Solution
    {
        private static Dictionary<int, HashSet<char>> DigitToCharSet = new Dictionary<int, HashSet<char>>{
            {0, new HashSet<char>("ABCEFG")},
            {1, new HashSet<char>("CF")},
            {2, new HashSet<char>("ACDEG")},
            {3, new HashSet<char>("ACDFG")},
            {4, new HashSet<char>("BCDF")},
            {5, new HashSet<char>("ABDFG")},
            {6, new HashSet<char>("ABDEFG")},
            {7, new HashSet<char>("ACF")},
            {8, new HashSet<char>("ABCDEFG")},
            {9, new HashSet<char>("ABCDFG")}
        };
        private static HashSet<char>[] GetCharSet(string s) {
            string[] strings = s.Split(' ');
            HashSet<char>[] results = new HashSet<char>[strings.Length];
            for(ushort idx=0; idx<strings.Length; idx++) {
                results[idx] = new HashSet<char>(strings[idx]);
            }
            return results;
        }
        private static Dictionary<char,char> GetMapping(HashSet<char>[] signals) {
            ushort twoCharIndex, threeCharIndex, fourCharIndex, sevenCharIndex;
            twoCharIndex = threeCharIndex = fourCharIndex = sevenCharIndex = 0;
            ushort[] sixCharIndex = new ushort[3];
            ushort[] fiveCharIndex = new ushort[3];
            ushort sixCharCursor = 0;
            ushort fiveCharCursor = 0;
            for (ushort idx=0; idx<10; idx++) {
                if (signals[idx].Count == 2) {twoCharIndex = idx;}
                else if (signals[idx].Count == 3) {threeCharIndex = idx;}
                else if (signals[idx].Count == 4) {fourCharIndex = idx;}
                else if (signals[idx].Count == 5) {
                    fiveCharIndex[fiveCharCursor] = idx;
                    fiveCharCursor++;
                } else if (signals[idx].Count == 6) {
                    sixCharIndex[sixCharCursor] = idx;
                    sixCharCursor++;
                } 
                else if (signals[idx].Count == 7) {sevenCharIndex = idx;}
            }
            Dictionary<char,char> mapping = new Dictionary<char, char>();
            // find {A}
            HashSet<char> A = new HashSet<char>(signals[threeCharIndex].Except(signals[twoCharIndex]));
            // find {CF}
            HashSet<char> CF = new HashSet<char>(signals[threeCharIndex].Intersect(signals[twoCharIndex]));
            // find {ADG} 
            HashSet<char> ADG = new HashSet<char>(signals[fiveCharIndex[0]].Intersect(signals[fiveCharIndex[1]]).Intersect(signals[fiveCharIndex[2]]));
            // find {BE}
            HashSet<char> BE = new HashSet<char>(
                signals[fiveCharIndex[0]]
                .Union(signals[fiveCharIndex[1]])
                .Union(signals[fiveCharIndex[2]])
                .Except(ADG).Except(CF)
            );
            // find {ABFG}
            HashSet<char> ABFG = new HashSet<char>(signals[sixCharIndex[0]].Intersect(signals[sixCharIndex[1]]).Intersect(signals[sixCharIndex[2]]));
            // find letters
            mapping['A'] = A.First();
            mapping['B'] = ABFG.Except(ADG).Except(CF).First();
            mapping['C'] = CF.Except(ABFG).First();
            mapping['D'] = ADG.Except(ABFG).First();
            mapping['E'] = BE.Except(ABFG).First();
            mapping['F'] = ABFG.Except(BE).Except(ADG).First();
            mapping['G'] = ABFG.Except(A).Except(CF).Except(BE).First();

            Dictionary<char,char> reverseMapping = new Dictionary<char,char>();
            foreach(KeyValuePair<char,char> keyValue in mapping) {
                reverseMapping[keyValue.Value] = keyValue.Key;
            }
            return reverseMapping;          
        }
        
        private static int GetOutputValues(string line) {
            string[] parts = line.Split(" | ");
            HashSet<char>[] signals = GetCharSet(parts[0]);
            Dictionary<char,char> mapping = GetMapping(signals);
            int result = 0;
            foreach(HashSet<char> output in GetCharSet(parts[1])) {
                HashSet<char> mapped = new HashSet<char>();
                foreach(char el in output) {
                    mapped.Add(mapping[el]);
                }
                foreach(KeyValuePair<int, HashSet<char>> keyValue in DigitToCharSet) {
                    if (keyValue.Value.SetEquals(mapped)) {
                        result = result * 10 + keyValue.Key;
                    }
                }
            }
            return result;
        }
        private static int Solve(string input) {
            int result = 0;
            foreach(string line in input.Split('\n')) {
                result += GetOutputValues(line);
            }
            return result;
        }

        public static void Main(string[] args) {
            string input = args[0];
            var watch = new System.Diagnostics.Stopwatch();
            watch.Start();
            int result = Solve(input);
            watch.Stop();
            Console.WriteLine("_duration: " + watch.Elapsed.TotalMilliseconds + "\n" + result);
        }
        
    }
}
