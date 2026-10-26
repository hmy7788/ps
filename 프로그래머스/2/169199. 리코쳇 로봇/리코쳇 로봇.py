from collections import deque

def solution(board):
    y, x = len(board), len(board[0])
    start_y, start_x = 0, 0
    
    for r in range(y):
        for c in range(x):
            if board[r][c] == 'R':
                start_y, start_x = r, c
                break
    
    dy, dx = [-1, 1, 0, 0], [0, 0, -1, 1]
    
    visited = [[0] * x for _ in range(y)]
    visited[start_y][start_x] = 1
    dq = deque([(start_y, start_x)])
    
    while dq:
        cy, cx = dq.popleft()
        if board[cy][cx] == 'G':
            return visited[cy][cx]-1
        
        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ny, nx = cy, cx
            
            while 0 <= ny + dy < y and 0 <= nx + dx < x and board[ny+dy][nx+dx] != 'D':
                ny += dy
                nx += dx
            
            
            if visited[ny][nx] == 0:
                visited[ny][nx] = visited[cy][cx] + 1
                dq.append((ny, nx))
                
    return -1