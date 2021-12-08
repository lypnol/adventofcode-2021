using System;
using System.Collections.Generic;


namespace Aoc
{
    class Solution
    {
        private static byte[][] Digits = new byte[10][] {
            new byte[7]{1,1,1,0,1,1,1}, // "ABCEFG"
            new byte[7]{0,0,1,0,0,1,0}, // "CF"
            new byte[7]{1,0,1,1,1,0,1}, // "ACDEG"
            new byte[7]{1,0,1,1,0,1,1}, // "ACDFG"
            new byte[7]{0,1,1,1,0,1,0}, // "BCDF"
            new byte[7]{1,1,0,1,0,1,1}, // "ABDFG"
            new byte[7]{1,1,0,1,1,1,1}, // "ABDEFG"
            new byte[7]{1,0,1,0,0,1,0}, // "ACF"
            new byte[7]{1,1,1,1,1,1,1}, // "ABCDEFG"
            new byte[7]{1,1,1,1,0,1,1} // "ABCDFG"
        };

        private static void Union(byte[] left, byte[] right, byte[] output) {
            for (byte idx=0; idx<7; ++idx) {
                if (left[idx] + right[idx] > 0) {output[idx] = 1;}
                else {output[idx] = 0;}
            }
        }
        private static void Intersect(byte[] left, byte[] right, byte[] output) {
            for (byte idx=0; idx<7; ++idx) {
                if (left[idx] + right[idx] > 1) {output[idx] = 1;}
                else {output[idx] = 0;}
            }
        }
        private static void Except(byte[] left, byte[] right, byte[] output) {
            for (byte idx=0; idx<7; ++idx) {
                if (1 + left[idx] - right[idx] == 2) {output[idx] = 1;}
                else {output[idx] = 0;}
            }
        }
        private static byte First(byte[] input) {
            for (byte idx=0; idx<7; ++idx) {
                if (input[idx] == 1) {return idx;}
            }
            return 99;
        }
        private static bool Equal(byte[] left, byte[] right) {
            for (byte idx=0; idx<7; ++idx) {
                if (left[idx] != right[idx]) {return false;}
            } 
            return true;
        }

        private static byte[] GetMapping(byte[][] signals) {
            ushort twoCharIndex, threeCharIndex, fourCharIndex, sevenCharIndex;
            twoCharIndex = threeCharIndex = fourCharIndex = sevenCharIndex = 0;
            ushort[] sixCharIndex = new ushort[3];
            ushort[] fiveCharIndex = new ushort[3];
            ushort sixCharCursor = 0;
            ushort fiveCharCursor = 0;
            ushort size = 0;
            for (ushort idx=0; idx<10; ++idx) {
                size = 0;
                for (ushort idx2=0; idx2<7; ++idx2) {
                    if (signals[idx][idx2] == 1) size++;
                }
                if (size == 2) {twoCharIndex = idx;}
                else if (size == 3) {threeCharIndex = idx;}
                else if (size == 4) {fourCharIndex = idx;}
                else if (size == 5) {
                    fiveCharIndex[fiveCharCursor] = idx;
                    fiveCharCursor++;
                } else if (size == 6) {
                    sixCharIndex[sixCharCursor] = idx;
                    sixCharCursor++;
                } 
                else if (size == 7) {sevenCharIndex = idx;}
            }
            // Console.WriteLine("signals[twoCharIndex]=["+String.Join(',', signals[twoCharIndex])+"]");
            // Console.WriteLine("signals[threeCharIndex]=["+String.Join(',', signals[threeCharIndex])+"]");
            // Console.WriteLine("signals[fourCharIndex]=["+String.Join(',', signals[fourCharIndex])+"]");
            // Console.WriteLine("signals[fiveCharIndex[0]]=["+String.Join(',', signals[fiveCharIndex[0]])+"]");
            // Console.WriteLine("signals[fiveCharIndex[1]]=["+String.Join(',', signals[fiveCharIndex[1]])+"]");
            // Console.WriteLine("signals[fiveCharIndex[2]]=["+String.Join(',', signals[fiveCharIndex[2]])+"]");
            // Console.WriteLine("signals[sixCharIndex[0]]=["+String.Join(',', signals[sixCharIndex[0]])+"]");
            // Console.WriteLine("signals[sixCharIndex[1]]=["+String.Join(',', signals[sixCharIndex[1]])+"]");
            // Console.WriteLine("signals[sixCharIndex[2]]=["+String.Join(',', signals[sixCharIndex[2]])+"]");
            // Console.WriteLine("signals[sevenCharIndex]=["+String.Join(',', signals[sevenCharIndex])+"]");
            // find {A}
            byte[] A = new byte[7];
            Except(signals[threeCharIndex], signals[twoCharIndex], A);
            // find {CF}
            byte[] CF = signals[twoCharIndex];
            // find {ADG}
            byte[] ADG = new byte[7];
            Intersect(signals[fiveCharIndex[0]], signals[fiveCharIndex[1]], ADG);
            Intersect(ADG, signals[fiveCharIndex[2]], ADG);
            // find {BE}
            byte[] BE = new byte[7];
            Except(signals[sevenCharIndex], ADG, BE);
            Except(BE, CF, BE);
            // find {ABFG}
            byte[] ABFG = new byte[7];
            Intersect(signals[sixCharIndex[0]], signals[sixCharIndex[1]], ABFG);
            Intersect(ABFG, signals[sixCharIndex[2]], ABFG);
            // find letters
            byte[] mapping = new byte[7];
            mapping[0] = First(A);
            byte[] B = new byte[7];
            Except(ABFG, ADG, B);
            Except(B, CF, B);
            mapping[1] = First(B);
            byte[] C = new byte[7];
            Except(CF, ABFG, C);
            mapping[2] = First(C);
            byte[] D = new byte[7];
            Except(ADG, ABFG, D);
            mapping[3] = First(D);
            byte[] E = new byte[7];
            Except(BE, ABFG, E);
            mapping[4] = First(E);
            byte[] F = new byte[7];
            Except(ABFG, BE, F);
            Except(F, ADG, F);
            mapping[5] = First(F);
            byte[] G = new byte[7];
            Except(ABFG, A, G);
            Except(G, CF, G);
            Except(G, BE, G);
            mapping[6] = First(G);
            // Console.WriteLine("A=["+String.Join(',', A)+"]");
            // Console.WriteLine("B=["+String.Join(',', B)+"]");
            // Console.WriteLine("C=["+String.Join(',', C)+"]");
            // Console.WriteLine("D=["+String.Join(',', D)+"]");
            // Console.WriteLine("E=["+String.Join(',', E)+"]");
            // Console.WriteLine("F=["+String.Join(',', F)+"]");
            // Console.WriteLine("G=["+String.Join(',', G)+"]");
            // Console.WriteLine("mapping=["+String.Join(',', mapping)+"]");
            byte[] reverseMapping = new byte[7];
            for (byte idx=0; idx<7; ++idx) {
                reverseMapping[mapping[idx]] = idx;
            }
            return reverseMapping;          
        }
        
        private static int GetOutputValues(byte[][] signals) {
            byte[] mapping = GetMapping(signals);
            int result = 0;
            for (ushort idx=10; idx<14; ++idx) {
                byte[] mapped = new byte[7];
                for (ushort idx2=0; idx2<7; ++idx2) {
                    if (signals[idx][idx2] == 1) {
                        mapped[mapping[idx2]] = 1;
                    }
                }
                for (ushort idx2=0; idx2<10; ++idx2) {
                    if (Equal(mapped, Digits[idx2])) {
                        result = result * 10 + idx2;
                    }
                }
            }
            return result;
        }
        private static void ResetSignals(byte[][] signals) {
            for (ushort x=0; x<14; ++x) {
                for (ushort y=0; y<7; ++y) {
                    signals[x][y] = 0;
                }
            }
        }
        private static int Solve(char[] input) {
            int result = 0;
            ushort cursor = 0;
            byte[][] signals = new byte[14][];
            for (ushort idx2=0; idx2<14; ++idx2) {
                signals[idx2] = new byte[7];
            }
            ushort idx = 0;
            while (cursor < (ushort) input.Length) {
                switch (input[cursor]) {
                    case '\n':
                        result += GetOutputValues(signals);
                        ResetSignals(signals);
                        idx = 0;
                        break;
                    case '|':
                        --idx;
                        break;
                    case ' ':
                        ++idx;
                        break;
                    default:
                        signals[idx][(int)(input[cursor]-'a')] = 1;
                        break;
                }
                ++cursor;
            }          
            result += GetOutputValues(signals);
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
