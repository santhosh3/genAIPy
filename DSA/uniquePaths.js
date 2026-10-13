
function uniquePaths(m, n) {
    const dfs = (row, col, memo) => {
        if (row >= m || col >= n) {
            return 0;
        }

        if (row == m - 1 && col == n - 1) {
            return 1;
        }

        let key = `${row}.${col}`;

        if (memo.has(key)) {
            return memo.get(key)
        }

        let result = dfs(row + 1, col, memo) + dfs(row, col + 1, memo);
        memo[key] = result;
        return result;
    }
    return dfs(0, 0, new Map());
}

let m = 3, n = 7
console.log(uniquePaths(m, n))



