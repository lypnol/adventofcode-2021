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

        private static int FuelConsumption(int from, int to) {
            if (from < to) {
                return (to-from) * (to-from+1) / 2; 
            } else { 
                return (from-to) * (from-to+1) / 2;
            }
        }

        private static int TotalFuelConsumption(int[] positions, int size, int target) {
            int result = 0;
            for (int idx=0; idx<size; idx++) {
                result += FuelConsumption(positions[idx], target);
            }
            return result;
        }
        private static int Solve(char[] input) {
            (int[] positions, int size) = Parse(input);
            int sum = 0;
            for (int idx=0; idx<size; idx++) {
                sum += positions[idx];
            } 
            int target = (int) Math.Round(((double) sum / (double) size)); // mean
            
            int currentBest = TotalFuelConsumption(positions, size, target);
            int current = currentBest;
            while (true) {
                target--;
                current = TotalFuelConsumption(positions, size, target);
                if (current < currentBest) {
                    currentBest = current;
                } else { return currentBest;}
            }
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
