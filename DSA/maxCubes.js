
function findMaxCubes(input) {
    let memo = {}
    let maxSquareSide = 0
    for(let row = 0; row < input.length; row++) {
        for(let col = 0; col < input[row].length; col++) {
            let currentCube = _findMaxCubes(input, row, col, memo)
            maxSquareSide = Math.max(maxSquareSide, currentCube);
        }
    }
    return maxSquareSide * maxSquareSide;
}

function _findMaxCubes(input, row, col, memo) {
    if(row >= input.length || col >= input[row].length) {
        return 0
    }

    let key = `${row}.${col}`;

    if(key in memo) {
        return memo[key];
    }

    if(input[row][col] === 0) {
        memo[key] = 0
        return 0
    }

    let down = _findMaxCubes(input, row + 1, col, memo);
    let right = _findMaxCubes(input, row, col + 1, memo);
    let diagonal = _findMaxCubes(input, row + 1, col + 1, memo);
    let maxSide = 1 + Math.min(down, right, diagonal)
    memo[key] = maxSide;
    return memo[key];
}

let input = [
    [1, 0, 1, 0, 0],
    [1, 0, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 0, 1, 1, 1]
]

console.log(findMaxCubes(input))