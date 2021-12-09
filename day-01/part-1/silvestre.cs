namespace Aoc {
    class Solution {

        private static int solve(char[] input){
            int counter = 0;
            int previous_depth = int.MaxValue;
            int current_depth = 0;
            for(int index=0; index < input.Length; index++){
                if (input[index] == '\n'){
                    if (current_depth > previous_depth){
                        counter++;
                    }
                    previous_depth = current_depth;
                    current_depth = 0;
                } else {
                    current_depth = current_depth * 10 + (int)(input[index] - '0');
                }
            }
            if (current_depth != 0 && current_depth > previous_depth) counter++;

            return counter;
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