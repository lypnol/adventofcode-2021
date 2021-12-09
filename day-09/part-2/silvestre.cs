using System;
using System.Collections.Generic;


namespace Aoc
{
    class Solution
    {
        private const ushort LINE_LENGTH = 100+1;
        private const ushort N_LINES = 100;
        private static int BassinSize(char[] input, ushort cursor, ushort col) {
            int size = 0;
            ushort current;
            Stack<ushort> toVisit = new Stack<ushort>();
            byte[] visited = new byte[N_LINES*LINE_LENGTH];
            toVisit.Push(cursor);
            while (toVisit.Count > 0) {
                if (toVisit.Count == 0) continue;
                current = toVisit.Pop();
                if (visited[current] == 1 || input[current] == '\n' || input[current] == '9') {
                    visited[current] = 1;
                    continue;
                } else {
                    ++size;
                    visited[current] = 1;
                    if (current >= LINE_LENGTH && visited[current-LINE_LENGTH] == 0) {
                        toVisit.Push((ushort)(current-LINE_LENGTH));
                    }
                    if (current < LINE_LENGTH * (N_LINES-1) && visited[current+LINE_LENGTH] == 0) {
                        toVisit.Push((ushort)(current+LINE_LENGTH));
                    }
                    if ((current < LINE_LENGTH * N_LINES - 2) && visited[current+1] == 0) {
                        toVisit.Push((ushort)(current+1));
                    }
                    if (current > 0  && visited[current-1] == 0) {
                        toVisit.Push((ushort)(current-1));
                    }
                }
            }
            return size;
        }
        private static bool IsLowPoint(char[] input, ushort cursor, ushort col) {
            return (
                ((cursor < LINE_LENGTH) || (input[cursor] < input[cursor-LINE_LENGTH])) &&
                ((cursor >= LINE_LENGTH * (N_LINES-1)) || (input[cursor] < input[cursor+LINE_LENGTH])) &&
                ((col == 1) || (input[cursor] < input[cursor-1])) &&
                ((col == LINE_LENGTH-1) || (input[cursor] < input[cursor+1]))
            );
        }
        private static int Solve(char[] input) {
            int top1, top2, top3, current;
            top1 = top2 = top3 = current = 0;
            ushort cursor = 0;
            ushort col = 1;
            while (cursor < LINE_LENGTH * N_LINES - 1) {
                if (input[cursor] == '\n') {col = 0;}
                else if (IsLowPoint(input, cursor, col)) {
                    current = BassinSize(input, cursor, col);
                    if (current > top1) {top3 = top2; top2 = top1; top1 = current;}
                    else if (current > top2) {top3 = top2; top2 = current;}
                    else if (current > top3) {top3 = current;}
                }
                ++col;
                ++cursor;
            }
            return top1 * top2 * top3;
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
