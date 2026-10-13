
function targetSum(nums, target) {
    let count = 0;
    const dfs = (i, sum) => {
        if(i == nums.length) {
            if(sum == target) {
                count++
            }
            return
        }
        dfs(i + 1, sum + nums[i]);
        dfs(i + 1, sum - nums[i]);
    }
    dfs(0, 0);
    return count;
}


// let nums = [1,1,1,1,1], target = 3; 
// console.log(targetSum(nums, target))

function minimumTotal(triangle) {
    const memo = new Map();

    function dfs(row, col) {
        if (row == triangle.length - 1) {
            return triangle[row][col];
        }

        const key = `${row}.${col}`;

        if (memo.has(key)) {
            return memo.get(key);
        }

        const down = dfs(row + 1, col);
        const diagonal = dfs(row + 1, col + 1);

        const ans = triangle[row][col] + Math.min(down, diagonal);
        memo.set(key, ans);
        return ans;
    }

    dfs(0, 0);
}