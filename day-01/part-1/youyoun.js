const {performance} = require("perf_hooks");

/**
 * @param {string} s puzzle input in string format
 * @returns {string} solution flag
 */
const run = (s) => {
    // Your code goes here
    s_split = s.split("\n").map(x => parseInt(x));
    counter = 0
    for (i = 0; i < s_split.length - 1; i++) {
        if (s_split[i + 1] > s_split[i]) {
            counter += 1
        }
    }
    return counter;
};

const start = performance.now();
const answer = run(process.argv[2]);

console.log(`_duration:${performance.now() - start}`);
console.log(answer);
