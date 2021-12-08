const {performance} = require("perf_hooks");

const countSplitOnes = (arr, bitPosition) => {
    let onesCounter = 0;
    let onesArray = [];
    let zerosArray = [];
    for (let i = 0; i < arr.length; i++) {
        if (arr[i][bitPosition] === '1') {
            onesCounter += 1;
            onesArray.push(arr[i])
        } else {
            zerosArray.push(arr[i])
        }
    }
    return [onesCounter, onesArray, zerosArray]
};

const getBinNumArray = (arr, most) => {
    let binNumLen = arr[0].length;
    for (let bitPosition = 1; bitPosition < binNumLen; bitPosition++) {
        [nOnes, onesArray, zerosArray] = countSplitOnes(arr, bitPosition);
        if (nOnes >= arr.length / 2) {
            arr = most ? onesArray : zerosArray;
        } else {
            arr = most ? zerosArray : onesArray;
        }
        if (arr.length === 1) break;
    }
    return arr;
};

const binStr2dec = (binStr) => {
    let bin = 0;
    for (let i = binStr.length - 1; i >= 0; i--) {
        bin += parseInt(binStr[i]) * 2 ** (binStr.length - i - 1);
    }
    return bin;
}

/**
 * @param {string} s puzzle input in string format
 * @returns {string} solution flag
 */
const run = (s) => {
    // Your code goes here
    let sSplit = s.split("\n");
    const binNum = sSplit.length;

    [nOnes, onesArray, zerosArray] = countSplitOnes(sSplit, 0);
    let mostIndexArray;
    let leastIndexArray;
    if (nOnes > binNum / 2) {
        mostIndexArray = onesArray;
        leastIndexArray = zerosArray;
    } else {
        mostIndexArray = zerosArray;
        leastIndexArray = onesArray;
    }
    mostIndexArray = getBinNumArray(mostIndexArray, true);
    leastIndexArray = getBinNumArray(leastIndexArray, false);
    return binStr2dec(mostIndexArray[0]) * binStr2dec(leastIndexArray[0]);
};

const start = performance.now();
const answer = run(process.argv[2]);

console.log(`_duration:${performance.now() - start}`);
console.log(answer);
