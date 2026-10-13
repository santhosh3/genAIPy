// function minEatSpeed(piles, h) {
//     let right = Math.max(...piles);
//     let result = right;
//     let left = 1;
//     while (left <= right ) {
//         let mid = Math.ceil((left + right)/2);
//         let hours = 0
//         for(let pile of piles) {
//            hours += Math.ceil(pile/mid);
//         }

//         if(hours > h) {
//             left = mid + 1;
//         } else {
//             result = Math.min(result, mid);
//             right = mid - 1;
//         }
//     }
//     return result;

//     // for(let i = 1; i <= Math.max(...piles); i++) {
//     //     let hours = 0
//     //     for(let j = 0; j < piles.length; j++) {
//     //         let pile = piles[j];
//     //         hours += Math.ceil(pile/i); 
//     //     }
//     //     if(result > hours) {
//     //         result = hours;
//     //     }
//     // }
//     // return result;
// }

function minEatSpeedRec(piles, h) {
    let right = Math.max(...piles);

    function binarySearch(left, right, result) {
        if(left > right) return result;

        let hours = piles.reduce((acc, pile) => {
            return acc + Math.ceil(pile / Math.ceil((left + right) / 2))
        },0);

        if(hours > h) {
            return binarySearch(mid + 1, right, result)
        } else {
            return binarySearch(left, mid - 1, Math.min(result, mid))
        }
    }

   return binarySearch(1, right, right)
}

let piles = [3, 6, 7, 11], h = 8;
console.log(minEatSpeedRec(piles, h));






