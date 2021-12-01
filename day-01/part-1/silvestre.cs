namespace Aoc {
    class Solution {

        private static int fastIntParse(string input) {
            int result = 0;
            for(int idx=0; idx<input.Length; idx++){
                result = result * 10 + ((int) input[idx]);
            }
            return result;
        }

        private static string solve(string input){
            int counter = 0;
            int previous_depth = int.MaxValue;
            int current_depth;
            foreach(string line in input.Split('\n')){
                current_depth = fastIntParse(line);
                if(current_depth > previous_depth){
                    counter ++;
                }
                previous_depth = current_depth;
            }
            return Convert.ToString(counter);
        }

        public static void Main(string[] args) {
            string input = args[0];
            var watch = new System.Diagnostics.Stopwatch();
            watch.Start();
            string result = solve(input);
            watch.Stop();
            Console.WriteLine("_duration: " + watch.Elapsed.TotalMilliseconds + "\n" + result);
        }
    }
}