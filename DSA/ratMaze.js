function ratinaMaze(maze) {
    let n = maze.length;
    let result = [];

    let direction = [
        { direction : 'd', dr : 1, dc : 0 },
        { direction : 'u', dr : -1, dc : 0 },
        { direction : 'r', dr : 0, dc : 1 },
        { direction : 'l', dr : 0, dc : -1 }
    ]

    function backTrack(r,c,currentPath) {

        if(r == n - 1 && c == n - 1) {
            result.push(currentPath);
            return
        }

        maze[r][c] = 0;

        for(let dir of direction) {
            let nr = dir['dr'] + r;
            let nc = dir['dc'] + c;

            if(nr >= 0 && nr < n && nc >= 0 && nc < n && maze[nr][nc] == 1) {
                backTrack(nr, nc, currentPath + dir.direction)
            }
        }

        maze[r][c] = 1;
    }

    backTrack(0,0,'');
    return [...new Set(result)]
}

let maze = [
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 0, 0, 1, 1, 1, 0, 1],
    [0, 0, 1, 1, 0, 0, 1, 0, 1, 1],
    [1, 1, 0, 1, 1, 1, 1, 1, 1, 0],
    [1, 0, 1, 1, 0, 1, 0, 0, 1, 1],
    [1, 1, 1, 0, 1, 1, 1, 0, 0, 1],
    [0, 0, 1, 1, 1, 0, 1, 1, 1, 1],
    [1, 1, 1, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 0, 0, 0, 1, 0, 1, 1]
]

console.log(ratinaMaze(maze))

