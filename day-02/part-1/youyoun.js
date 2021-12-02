const {performance} = require("perf_hooks");


const forward = (pos, value) => {
    pos[0] += value;
};

const down = (pos, value) => {
    pos[1] += value;
};

const up = (pos, value) => {
    pos[1] -= value;
};

const keywords_op = {
    "forward": forward,
    "down": down,
    "up": up
};

/**
 * @param {string} s puzzle input in string format
 * @returns {number} solution flag
 */
const run = (s) => {
    let sSplit = s.split("\n");
    let pos = [0, 0];
    let instruction;
    for (let i = 0; i < sSplit.length; i++) {
        instruction = sSplit[i].split(" ");
        keywords_op[instruction[0]](pos, parseInt(instruction[1]));
    }
    return pos[0] * pos[1];
};


const start = performance.now();
const answer = run(process.argv[2]);

console.log(`_duration:${performance.now() - start}`);
console.log(answer);
