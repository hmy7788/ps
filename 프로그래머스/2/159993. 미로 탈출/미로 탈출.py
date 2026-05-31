from collections import deque

def bfs(g, start_idx, end_idx):
    dq = deque()
    y, x = len(g), len(g[0])
    visited = [[-1 for _ in range(x)] for _ in range(y)]
    visited[start_idx[0]][start_idx[1]] = 0
    dq.append(start_idx)
    
    while dq:
        point = dq.popleft()
        cur_y, cur_x = point[0], point[1]
        
        for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            next_y, next_x = cur_y + dy, cur_x +dx
                
            if not (0 <= next_y <= y-1 and 0 <= next_x <= x-1): continue
            if visited[next_y][next_x] != -1 or g[next_y][next_x] != 'O': continue
            
            visited[next_y][next_x] = visited[cur_y][cur_x] + 1
            dq.append((next_y, next_x))
            if visited[end_idx[0]][end_idx[1]] != -1:
                return visited[end_idx[0]][end_idx[1]]
        
    return -1 
    

def solution(maps):
    y = len(maps)
    x = len(maps[0])
    g = [['O' for _ in range(x)] for _ in range(y)]
    start_idx = None
    lever_idx = None
    exit_idx = None
    
    for i, row in enumerate(maps):
        for j, ch in enumerate(row):
            if ch in ('S', 'L', 'E', 'O'):
                g[i][j] = 'O'
                if ch == 'S': start_idx = (i, j)
                elif ch == 'L': lever_idx = (i, j)
                elif ch == 'E': exit_idx = (i, j)
            else:
                g[i][j] = 'X'
                
    # S -> L
    s_to_l = bfs(g, start_idx, lever_idx)
    # L -> E
    l_to_e = bfs(g, lever_idx, exit_idx)
    
    if s_to_l == -1 or l_to_e == -1:
        return -1
    else:
        return s_to_l + l_to_e