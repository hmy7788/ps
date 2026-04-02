from collections import deque

def bfs(maps):
    n, m = len(maps), len(maps[0])
    dq = deque()
    dq.append((0,0))
    dx = [-1, 1, 0, 0]
    dy = [0, 0, -1, 1]
    
    while dq:
        x, y = dq.popleft()
        
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            
            # 범위 체크
            if nx < 0 or nx >= n or ny < 0 or ny >= m:
                continue
            
            # 벽 체크
            if maps[nx][ny] == 0: continue
                
            if maps[nx][ny] == 1:
                maps[nx][ny] = maps[x][y] + 1
                dq.append((nx, ny))
                
    answer = maps[n-1][m-1]
    if answer == 1: return -1
    else: return answer
            
            
def solution(maps):
    return bfs(maps)