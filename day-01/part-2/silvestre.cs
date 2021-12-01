namespace Aoc
{
    class Solution
    {

        private static int fastIntParse(string input) {
            int result = 0;
            for(int idx=0; idx<input.Length; idx++){
                result = result * 10 + ((int) input[idx]);
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