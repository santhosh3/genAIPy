let obj = {
    a: {
        a1: {
            a2: 3,
            a3: {
                a4: 4
            }
        },
        a12: {
            a122: 123
        }
    },
    b: {
        b1: 1,
        b2: 2,
        b3: {
            b33: 3
        }
    }
}

function generateMapping(obj, ans, path = "") {
    for (let el in obj) {
        let currentPath = path ? `${path}.${el}` : el;
        if (typeof obj[el] !== "object") {
            ans[currentPath] = obj[el];
        } else {
            generateMapping(obj[el], ans, currentPath);
        }
    }
    return ans;
}


console.log(generateMapping(obj, {}))



