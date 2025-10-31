import sys
from collections import deque

def BFS(MAP, M, N, q):
    while(q):
        cp = q.popleft()
        cy, cx = cp[0], cp[1]
        for dx, dy in ((-1, 0), (1, 0), (0, 1), (0, -1)):
            ny, nx = cy+dy, cx+dx
            if(0 <= ny < N and
               0 <= nx < M and
               MAP[ny][nx] == 0):
                MAP[ny][nx] = MAP[cy][cx] + 1
                q.append([ny, nx])
    
    max_day = -1
    for y in range(N):
        for x in range(M):
            if(MAP[y][x] == 0): return -1
            if(max_day < MAP[y][x]): max_day = MAP[y][x]
    return max_day-1

input = sys.stdin.readline
M, N = map(int, input().split())
MAP = []
q = deque()
for _ in range(N):
    MAP.append(list(map(int, input().split())))

for y in range(N):
    for x in range(M):
        if(MAP[y][x] == 1): q.append([y, x])

print(BFS(MAP, M, N, q))