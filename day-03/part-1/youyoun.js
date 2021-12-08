const { performance } = require("perf_hooks");

/**
 * @param {string} s puzzle input in string format
 * @returns {string} solution flag
 */
const run = (s) => {
    let sSplit = s.split("\n");
    const binNumLen = sSplit[0].length;
    const binNum = sSplit.length;
    let oneCounter = new Array(binNumLen).fill(0);
    for (let i=0; i<binNum; i++) {
        for (let j=0; j<binNumLen; j++) {
            oneCounter[j] += parseInt(sSplit[i][j])
        }
    }
    let epsilon_rate = 0;
    let gamma_rate = 0;
    let bit;
    for (let i=binNumLen-1; i>=0; i--) {
        bit = (oneCounter[i] > (binNum / 2)) ? 1 : 0;
        epsilon_rate += bit * 2 ** (binNumLen - i - 1);
        gamma_rate += ((bit === 1) ? 0 : 1)  * 2 ** (binNumLen - i - 1);
    }
    return epsilon_rate * gamma_rate;
};

const start = performance.now();
const answer = run(process.argv[2]);

console.log(`_duration:${performance.now() - start}`);
console.log(answer);
