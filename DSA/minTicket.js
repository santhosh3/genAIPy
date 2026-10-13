function lowerBound(days, target) {
    let left = 0;
    let right = days.length;
    while (left < right) (days[Math.floor((left + right) / 2)] >= target) ? right = Math.floor((left + right) / 2) : left = Math.floor((left + right) / 2) + 1;
    return left;
}

function minTicketCosts(days, costs) {
    const memo = new Map();

    const minCost = (i) => {
        if (i >= days.length) return 0;
        if (memo.has(i)) return memo.get(i);
        
        const result = Math.min(
            costs[1] + minCost(i + 1),
            costs[7] + minCost(lowerBound(days, days[i] + 7)),
            costs[30] + minCost(lowerBound(days, days[i] + 30))
        );
        memo.set(i, result);
        return result;
    };

    const fairPrice = minCost(0);

    const result = [];

    const collectPossibilities = (i, slate) => {
        if (i >= days.length) {
            result.push([...slate]);
            return;
        }

        const passes = Object.keys(costs).map((item) => {
            const duration = Number(item);
            return {
                name: `${duration}-day`,
                price: costs[duration],
                next: lowerBound(days, days[i] + duration)
            };
        });

        for (const pass of passes) {
            if (pass.price + minCost(pass.next) !== minCost(i)) {
                continue;
            }

            slate.push({
                day: days[i],
                pass: pass.name,
                cost : pass.price
            });

            collectPossibilities(pass.next, slate);

            slate.pop();
        }
    };

    collectPossibilities(0, []);
    return {
        minCost: fairPrice,
        result : JSON.stringify(result)
    };
}

const days = [1, 4, 6, 7, 8, 20];

const costs = {
    1: 2,
    7: 7,
    30: 15
};

console.log(minTicketCosts(days, costs));
