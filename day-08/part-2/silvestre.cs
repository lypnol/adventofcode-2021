using System;
using System.Collections.Generic;


namespace Aoc
{
    enum State {Signals, Outputs};
    class Solution
    {
        private static byte EIGHT = 254;
        private static bool IsPowerOfTwo(int input) {
            return input != 0 & (input & (input-1)) == 0;
        }

        private static byte Index(byte[] array, byte value) {
            for (byte idx=0; idx<10; ++idx) {
                if (array[idx] == value) return idx;
            }
            return 99;
        }
        private static uint Solve(char[] input) {
            uint result = 0;
            ushort cursor = 0;
            State state = State.Signals;
            byte[] digits = new byte[10]{0,0,0,0,0,0,0,0,EIGHT,0};
            byte[] len_fives = new byte[3];
            byte[] len_sixes = new byte[3];
            ushort five_idx = 0;
            ushort six_idx = 0;
            byte word_size = 0;
            byte current_digit = 0;
            uint current_output = 0;
            while (cursor < input.Length) {
                switch (input[cursor]) {
                    case '\n':
                        current_output = (10 * current_output + Index(digits, current_digit));                            
                        result += current_output;
                        current_output = 0;
                        state = State.Signals;
                        current_digit = 0;
                        word_size = 0;
                        break;
                    case '|':
                        while (six_idx > 0) {
                            --six_idx;
                            if (IsPowerOfTwo(((digits[4] | digits[7]) ^ len_sixes[six_idx]))) {
                                digits[9] = len_sixes[six_idx];
                            } else if (IsPowerOfTwo(((EIGHT ^ len_sixes[six_idx]) & digits[1]))) {
                                digits[6] = len_sixes[six_idx];
                            } else {
                                digits[0] = len_sixes[six_idx];
                            }
                        }
                        while (five_idx > 0) {
                            --five_idx;
                            if (IsPowerOfTwo((digits[6] ^ len_fives[five_idx]))) {
                                digits[5] = len_fives[five_idx];
                            } else if (IsPowerOfTwo((digits[9] ^ len_fives[five_idx]))) {
                                digits[3] = len_fives[five_idx];
                            } else {
                                digits[2] = len_fives[five_idx];
                            }
                        }
                        state = State.Outputs;
                        ++cursor;
                        break;
                    case ' ':
                        switch (state) {
                            case State.Signals:
                                switch (word_size) {
                                    case 2:
                                        digits[1] = current_digit;
                                        break;
                                    case 3:
                                        digits[7] = current_digit;
                                        break;
                                    case 4:
                                        digits[4] = current_digit;
                                        break;
                                    case 5:
                                        len_fives[five_idx] = current_digit;
                                        ++five_idx;
                                        break;
                                    case 6:
                                        len_sixes[six_idx] = current_digit;
                                        ++six_idx;
                                        break;
                                }
                                break;
                            case State.Outputs:
                                current_output = (10 * current_output + Index(digits, current_digit));
                                break;
                        }
                        current_digit = 0;
                        word_size = 0;
                        break;
                    default:
                        current_digit |= (byte)(2 << (input[cursor]-'a'));
                        ++word_size;
                        break;
                }
                ++cursor;
            }
            current_output = (10 * current_output + Index(digits, current_digit));
            result += current_output;
            return result;
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
