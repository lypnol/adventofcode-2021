using System;
using System.Collections.Generic;


namespace Aoc
{
    enum State {X1, X2, Y1, Y2};
    
    class Solution
    {   

        private static void UpdateGrid(int x1, int y1, int x2, int y2, ref byte[,] grid, ref ushort counter) {
            if (x1 == x2) {
                (int min, int max) = y1 < y2 ? (y1, y2) : (y2, y1);
                for (int y=min;y<=max;y++) {
                    grid[x1, y]++;
                    if (grid[x1, y] == 2) counter++; 
                }
            } else if (y1 == y2) {
                (int min, int max) = x1 < x2 ? (x1, x2) : (x2, x1);
                for (int x=min;x<=max;x++) {
                    grid[x, y1]++;
                    if (grid[x, y1] == 2) counter++; 
                }
            } else if (x1 < x2 && y1 < y2) {
                for (int z=0;z<=x2-x1;z++){
                    grid[x1+z, y1+z]++;
                    if (grid[x1+z, y1+z] == 2) counter++;
                }
            } else if (x1 < x2 && y1 > y2) {
                for (int z=0;z<=x2-x1;z++){
                    grid[x1+z, y1-z]++;
                    if (grid[x1+z, y1-z] == 2) counter++;
                }
            } else if (x1 > x2 && y1 < y2) {
                for (int z=0;z<=x1-x2;z++){
                    grid[x2+z, y2-z]++;
                    if (grid[x2+z, y2-z] == 2) counter++;
                }
            } else if (x1 > x2 && y1 > y2) {
                for (int z=0;z<=x1-x2;z++){
                    grid[x2+z, y2+z]++;
                    if (grid[x2+z, y2+z] == 2) counter++;
                }
            }
        }
        private static int Solve(char[] input) {
            byte[,] grid = new byte[1000,1000];
            ushort counter, index;
            counter = index = 0;

            int x1, x2, y1, num_acc;
            x1 = x2 = y1 = num_acc = 0;
            State state = State.X1;
            while (index < input.Length) {
                switch (state, input[index]) {
                    case (State.Y2, '\n'):
                        UpdateGrid(x1, y1, x2, num_acc, ref grid, ref counter);
                        state = State.X1;
                        num_acc = 0;
                        index++;
                        break;
                    case (State.X2, ','):
                        x2 = num_acc;
                        num_acc = 0;
                        index++;
                        state = State.Y2;
                        break;
                    case (State.Y1, ' '):
                        y1 = num_acc;
                        num_acc = 0;
                        index += 4;
                        state = State.X2;
                        break;
                    case (State.X1, ','):
                        x1 = num_acc;
                        num_acc = 0;
                        index++;
                        state = State.Y1;
                        break;
                    default:
                        num_acc = 10 * num_acc + (int)(input[index] - '0');
                        index++;
                        break;
                }
            }
            UpdateGrid(x1, y1, x2, num_acc, ref grid, ref counter);
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
