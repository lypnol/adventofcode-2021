using System;
using System.Collections;
using System.Collections.Generic;


namespace Aoc
{
    class TreeNode {
        public int count = 0;
        public TreeNode? child0;
        public TreeNode? child1; 
    }

    class Solution
    {
        private static int LINE_LENGHT = 12;

        private static void InitTree(TreeNode node, int depth) {
            if (depth == LINE_LENGHT) return;
            else {
                node.child0 = new TreeNode();
                InitTree(node.child0, depth+1);
                node.child1 = new TreeNode();
                InitTree(node.child1, depth+1);
            }
        }

        private static bool ShouldSelectChild1(TreeNode node, bool oxy) {
            return (node.child0.count == 0 ||(oxy ^ (node.child1.count < node.child0.count))) && node.child1.count != 0;
            
        }
        private static int GetRating(TreeNode node, int depth, int current, bool oxy) {
            if (depth == LINE_LENGHT) return current;
            else {
                return GetRating(
                    ShouldSelectChild1(node, oxy) ? node.child1 : node.child0, 
                    depth + 1,
                    ShouldSelectChild1(node, oxy) ? current + (1 << (LINE_LENGHT-depth-1)): current,
                    oxy
                );
            }
        }

        private static int solve(char[] input) {
            TreeNode tree = new TreeNode();
            InitTree(tree, 0);
            TreeNode node = tree;
            node.count++;
            for (int index = 0; index < input.Length; index++){
                if (input[index] == '\n'){
                    node = tree;
                    node.count++;
                } else {
                    if (input[index] == '1') {
                        node = node.child1;
                    } else {node = node.child0;}
                    node.count++;
                }
            }
            return GetRating(tree, 0 ,0, true) * GetRating(tree, 0 ,0, false);
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
