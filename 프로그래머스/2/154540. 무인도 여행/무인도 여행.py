from collections import deque

def solution(maps):
    y, x = len(maps), len(maps[0])
    visited = [[0] * x for _ in range(y)]
    result = []
    
    def BFS(i, j):
        cnt = 0
        dq = deque()
        dq.append((i, j))
        cnt += int(maps[i][j])
        visited[i][j] = 1
        
        while dq:
            cy, cx = dq.popleft()
            # 상하좌우
            for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                ny, nx = cy+dy, cx+dx
                if 0 <= ny < y and 0 <= nx < x and visited[ny][nx] == 0 and maps[ny][nx] != 'X':
                    dq.append((ny, nx))
                    cnt += int(maps[ny][nx])
                    visited[ny][nx] = 1
        return cnt
        
    for i in range(y):
        for j in range(x):
            if maps[i][j] != 'X' and visited[i][j] == 0:
                cnt = BFS(i, j)
                result.append(cnt)
                
    if result:
        result.sort()
        return result
    else:
        return [-1]