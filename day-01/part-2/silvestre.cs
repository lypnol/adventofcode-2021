namespace Aoc
{
    class Solution
    {

        private static int fastIntParse(string input) {
            int result = 0;
            for(int idx=0; idx<input.Length; idx++){
                result = result * 10 + (input[idx] - '0');
            }
            return result;
        }
        private static string solve(string input){
            int counter = 0;
            string[] lines = input.Split('\n');
            int[] depths = new int[lines.Length];
            for(int index=0; index<lines.Length;index++){
                depths[index] = fastIntParse(lines[index]);
            }
            for(int index=3; index<depths.Length;index++){
                if(depths[index] > depths[index-3]){
                    counter ++;
                }
            }
            return Convert.ToString(counter);
        }

        private static int solve(char[] input){
            int counter = 0;
            int depth3 = 0;
            int depth2 = 0;
            int depth1 = 0;
            int current_depth = 0;
            for(int index=0; index < input.Length; index++) {
                if (input[index] == '\n') {
                    if (current_depth > depth3) counter++;
                    depth3 = depth2;
                    depth2 = depth1;
                    depth1 = current_depth;
                    current_depth = 0;
                } else {
                    current_depth = current_depth * 10 + (int)(input[index] - '0');
                }
            }
            if (current_depth != 0 && current_depth > depth3) counter++;
            return counter - 3;
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