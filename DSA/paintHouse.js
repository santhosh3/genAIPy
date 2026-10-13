
function minCostPaintHouse(costs) {
    let memo = {}
    const explore = (i, preColour) => {
        if(i >= costs.length) return 0;
        const key = `${i},${preColour}`;
        if(memo[key]) return memo[key];

        let result = Infinity;

        for(let colour = 0; colour < 3; colour++) {
            if(colour === preColour) continue;
            result = Math.min(result, costs[i][colour] + explore(i+1, colour))
        }
        memo[key] = result;
        return result
    }
    return explore(0, -1)
}

let costs = [[17,2,17],[16,16,5],[14,3,19]];
console.log(minCostPaintHouse(costs))

function numDecodings(s) {
    let memo = new Map();

    const dfs = (i) => {
        if (i == s.length) return 1;
        if (s[i] == '0') return 0;
        if (memo.has(i)) return memo.get(i);
        let result = dfs(i + 1);
        if (i + 1 < s.length && Number(s.slice(i, i+2)) <= 26) {
            result += dfs(i + 2); 
        }
        memo.set(i, result);
        return result
    }
    return dfs(0)
}

console.log(numDecodings('226'))

var coinChange = function(coins, amount) {
    const memo = new Map();
    function dp(amount) {
        // Base case
        if (amount === 0) return 0;
        // Impossible
        if (amount < 0) return Infinity;
        if (memo.has(amount)) {
            return memo.get(amount);
        }
        let ans = Infinity;
        for (const coin of coins) {
            ans = Math.min( ans, 1 + dp(amount - coin));
        }
        memo.set(amount, ans);
        return ans;
    }
    const result = dp(amount);
    return result === Infinity ? -1 : result;
};

var deleteAndEarn = function(nums) {
    const count = new Map();

    // Count frequency
    for (const num of nums) {
        count.set(num, (count.get(num) || 0) + 1);
    }

    // Unique numbers
    const arr = [...new Set(nums)].sort((a, b) => a - b);

    const memo = new Map();

    function dp(i) {
        if (i < 0) return 0;

        if (memo.has(i)) {
            return memo.get(i);
        }

        // Points we get by taking arr[i]
        const points = arr[i] * count.get(arr[i]);

        // Don't take current number
        const skip = dp(i - 1);

        let take;

        if (i > 0 && arr[i] === arr[i - 1] + 1) {
            // Current and previous are consecutive
            take = points + dp(i - 2);
        } else {
            // Not consecutive
            take = points + dp(i - 1);
        }

        const ans = Math.max(skip, take);

        memo.set(i, ans);

        return ans;
    }

    return dp(arr.length - 1);
};
