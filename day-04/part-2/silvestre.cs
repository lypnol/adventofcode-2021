using System;
using System.Collections.Generic;


namespace Aoc
{
    class Solution
    {
        private static void PrintBoard(int[,] board){
            Console.Write("board=[");
            for (int rowIdx = 0; rowIdx < 5; rowIdx++) {
                for (int colIdx = 0; colIdx < 5; colIdx++) {
                    Console.Write(board[rowIdx, colIdx]+ " ");
                }
                Console.Write("\n");
            }
        }

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
                //Console.WriteLine($"toDraw={number}");
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
                    //Console.WriteLine($"rowCheck[{idx}] = {rowCheck[idx]}, colCheck[{idx}] = {colCheck[idx]}");
                    if ((rowCheck[idx] == 5 || colCheck[idx] == 5)) {
                        //Console.WriteLine($"drawIdx={drawIdx}, number={number}, total={total}");
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
            int maxDrawIdx = 0;
            int maxTotal = 0;
            while (cursor <= input.Length) {
                if (cursor == input.Length || input[cursor] == '\n') {
                    //Console.WriteLine($"NEWLINE x={x}, y={y}, number={number}");
                    board[x, y] = number;
                    number = 0;
                    y = 0;
                    x++;
                } else if (input[cursor] == ' ') {
                    if (input[cursor+1] != ' ' && input[cursor-1] != '\n') {
                        board[x, y] = number;
                        //Console.WriteLine($"x={x}, y={y}, number={number}");
                        number = 0;
                        y++;
                    }
                } else {number = 10 * number + (int)(input[cursor] - '0');}
                if (x == 5 && y == 0) {
                    //PrintBoard(board);
                    // check
                    (int drawIdx, int total) = CheckBoardWin(board, toDraw);
                    if (drawIdx > maxDrawIdx) {
                        maxDrawIdx = drawIdx;
                        maxTotal = total;
                    }
                    // reset
                    x = 0;
                    y = 0;
                    cursor++;
                }
                cursor++;
            }
            return maxTotal * toDraw[maxDrawIdx];
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
