from collections import deque
import sys

def BFS(I, x, y, n, m):
    visited = [[0]*I for _ in range(I)]
    visited[y][x] = 1
    q = deque()
    q.append([x, y, 0])

    while(q):
        cp = q.popleft()
        cx, cy, cc = cp[0], cp[1], cp[2]
        if(cx == n and cy == m): return cc
        for dx, dy in ((-2, -1), (-1, -2), (1, -2), (2, -1),
                       (2, 1), (1, 2), (-1, 2), (-2, 1)):
            nx, ny = cx + dx, cy + dy
            if(0 <= nx < I and
               0 <= ny < I and
               visited[ny][nx] == 0):
                q.append([nx, ny, cc+1])
                visited[ny][nx] = 1

input = sys.stdin.readline
T = int(input())
for _ in range(T):
    I = int(input())
    x, y = map(int, input().split())
    n, m = map(int, input().split())
    print(BFS(I, x, y, n, m))