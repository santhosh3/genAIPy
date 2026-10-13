function findWordFromBoard(board, word) {
    if (word.length === 0) return true;
    if (board.length === 0 || board[0].length === 0) return false;

    const rows = board.length;
    const cols = board[0].length;
    let visited = new Set();

    function dfs(r, c, i) {
        if (i === word.length) {
            return true;
        }

        if(r < 0 || r >= rows || c < 0 || c >= cols) return false;

        let key = `${r},${c}`;

        if(visited.has(key)) {
            return false;
        }

        if(board[r][c] !== word[i]) {
            return false
        }

        visited.add(key);

        const found = dfs(r + 1, c, i + 1) || 
                      dfs(r - 1, c, i + 1) || 
                      dfs(r, c + 1, i + 1) || 
                      dfs(r, c - 1, i + 1) 
        
        visited.delete(key);
        return found;
    }

    for(let r = 0; r < rows; r++) {
        for(let c = 0; c < cols; c++) {
           if(dfs(r,c,0)) {
              return true
           } 
        }
    }
    return false
}

const board = [
  ["C","H","A","R","A","C"],
  ["X","X","X","X","X","T"],
  ["S","C","I","T","S","I"],
  ["I","X","X","X","X","R"],
  ["T","S","I","R","E","T"],
  ["X","X","X","X","X","A"]
]
const word = "CXSCITXR"

console.log(findWordFromBoard(board,word))