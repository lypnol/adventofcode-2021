using System;
using System.Collections.Generic;


namespace Aoc
{
    class Solution
    {

        private static int GetBoardSum(int[,] board) {
            int total = 0;
            for (int rowIdx = 0; rowIdx < 5; rowIdx++) {
                for (int colIdx = 0; colIdx < 5; colIdx++) {
                    total += board[rowIdx, colIdx];
                }    
            }
            return total;
        }

        private static (int, int) CheckBoardWin(int[,] board, List<int> toDraw) {
            int total = GetBoardSum(board);
            int number = 0;
            int[] rowCheck = new int[5];
            int[] colCheck = new int[5];
            for (int drawIdx = 0; drawIdx < toDraw.Count; drawIdx++) {
                number = toDraw[drawIdx];
                for (int rowIdx = 0; rowIdx < 5; rowIdx++) {
                    for (int colIdx = 0; colIdx < 5; colIdx++) {
                        if (number == board[rowIdx, colIdx]) {
                            rowCheck[rowIdx]++;
                            colCheck[colIdx]++;
                            total -= number;
                        }
                    }    
                }
                for (int idx = 0; idx < 5; idx++) {
                    if ((rowCheck[idx] == 5 || colCheck[idx] == 5)) {
                        return (drawIdx, total);
                    }
                }
            }
            return (-1, -1);
        }

        
        private static int Solve(char[] input) {
            List<int> toDraw = new List<int>();
            int cursor = 0;
            int number = 0;
            while (input[cursor] != '\n') {
                if (input[cursor] == ',') {
                    toDraw.Add(number);
                    number = 0;
                } else {number = 10 * number + (int)(input[cursor] - '0');}
                cursor++;
            }
            number = 0;
            cursor += 2;
            
            int[,] board = new int[5,5];
            int x = 0;
            int y = 0;
            int minDrawIdx = int.MaxValue;
            int minTotal = 0;
            while (cursor <= input.Length) {
                if (cursor == input.Length || input[cursor] == '\n') {
                    board[x, y] = number;
                    number = 0;
                    y = 0;
                    x++;
                } else if (input[cursor] == ' ') {
                    if (input[cursor+1] != ' ' && input[cursor-1] != '\n') {
                        board[x, y] = number;
                        number = 0;
                        y++;
                    }
                } else {number = 10 * number + (int)(input[cursor] - '0');}
                cursor++;
                
                if (x == 5 && y == 0) {
                    (int drawIdx, int total) = CheckBoardWin(board, toDraw);
                    if (drawIdx < minDrawIdx) {
                        minDrawIdx = drawIdx;
                        minTotal = total;
                    }
                    x = 0;
                    y = 0;
                    cursor++;
                }
            }
            return minTotal * toDraw[minDrawIdx];
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
