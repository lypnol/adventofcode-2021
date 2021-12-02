const {performance} = require("perf_hooks");

const sumArray = (arr) => {
    return arr.reduce((a, b) => a + b)
};

/**
 * @param {string} s puzzle input in string format
 * @returns {number} solution flag
 */
const run = (s) => {
    // Your code goes here
    let sSplit = s.split("\n").map(x => parseInt(x));
    const windowSize = 3;
    let counter = 0;
    for (i = 0; i < sSplit.length - windowSize; i++) {
        if (sumArray(sSplit.slice(i + 1, i + 1 + windowSize)) > sumArray(sSplit.slice(i, i + windowSize))) {
            counter += 1;
        }
    }
    return counter;
};

const start = performance.now();
const answer = run(process.argv[2]);

console.log(`_duration:${performance.now() - start}`);
console.log(answer);
