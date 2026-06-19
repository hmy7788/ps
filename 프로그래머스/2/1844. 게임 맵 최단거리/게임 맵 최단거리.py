from collections import deque
            
def solution(maps):
    y, x = len(maps), len(maps[0])
    dq = deque()
    dq.append((0, 0))
    
    while dq:
        cy, cx = dq.popleft()
        for dy, dx in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            ny, nx = cy+dy, cx+dx
            if 0 <= ny < y and 0 <= nx < x and maps[ny][nx] == 1:
                maps[ny][nx] = maps[cy][cx] + 1
                dq.append((ny, nx))
    
    answer = maps[y-1][x-1]
    return answer if answer != 1 else -1