using System;
using System.Collections;
using System.Collections.Generic;


namespace Aoc
{
    class Solution
    {
        private static int LINE_LENGHT = 12;

        private static bool ShouldSelectChild1(ushort[] heap, int heap_index, bool oxy) {
            return heap[2*heap_index+1] != 0 && (heap[2*heap_index+2] == 0 ||(oxy ^ (heap[2*heap_index+1] < heap[2*heap_index+2]))) ;
            
        }
        private static int GetRating(ushort[] heap, bool oxy) {
            int heap_index = 0;
            int depth = 0;
            int rating = 0;
            while (depth < LINE_LENGHT){
                if(ShouldSelectChild1(heap, heap_index, oxy)){
                    heap_index = 2 * heap_index + 1;
                    rating += (1 << (LINE_LENGHT-depth-1));
                } else {
                    heap_index = 2 * heap_index + 2;
                }
                depth++;
            }
            return rating;
        }

        private static int solve(char[] input) {
            int heap_size = (1<<(LINE_LENGHT+2)-1);
            ushort[] heap = new ushort[heap_size];
            int heap_index = 0;
            heap[heap_index]++;
            for (int index = 0; index < input.Length; index++){
                if (input[index] == '\n'){
                    heap_index = 0;
                } else {
                    if (input[index] == '1') {
                        heap_index = 2*heap_index + 1;
                    } else {heap_index = 2*heap_index+2;}
                }
                heap[heap_index]++;
            }
            return GetRating(heap, true) * GetRating(heap, false);
        }

        public static void Main(string[] args) {
            char[] input = args[0].ToCharArray();
            var watch = new System.Diagnostics.Stopwatch();
            watch.Start();
            int result = solve(input);
            watch.Stop();
            Console.WriteLine("_duration: " + watch.Elapsed.TotalMilliseconds + "\n" + result);
        }
        
    }
}
