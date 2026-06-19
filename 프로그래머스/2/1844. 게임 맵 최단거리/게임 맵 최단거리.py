from collections import deque
            
def solution(maps):
    y, x = len(maps), len(maps[0])
    dq = deque()
    dq.append((0, 0))
    v = [[0 for _ in range(x)] for _ in range(y)] 
    v[0][0] = 1
    
    while dq:
        cy, cx = dq.popleft()
        for dy, dx in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            ny, nx = cy+dy, cx+dx
            if 0 <= ny < y and 0 <= nx < x and maps[ny][nx] != 0 and v[ny][nx] == 0:
                maps[ny][nx] = maps[cy][cx] + 1
                dq.append((ny, nx))
                v[ny][nx] = 1
    
    answer = maps[y-1][x-1]
    return answer if answer != 1 else -1