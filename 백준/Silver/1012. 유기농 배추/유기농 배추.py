import sys
from collections import deque

def BFS(MAP, N, M, visited, x, y):
    q = deque()
    q.append([y, x])
    visited[y][x] = 1

    while(q):
        cp = q.popleft()
        cy, cx = cp[0], cp[1]
        for dy, dx in ((-1, 0), (0, -1), (1, 0), (0, 1)):
            ny, nx = cy + dy, cx + dx
            if(0 <= ny < N and
               0 <= nx < M and
               MAP[ny][nx] == 1 and
               visited[ny][nx] == 0):
                q.append([ny, nx])
                visited[ny][nx] = 1

def solution(MAP, N, M):
    visited = [[0] * M for _ in range(N)]
    cnt = 0
    for y in range(N):
        for x in range(M):
            if(MAP[y][x] == 1 and visited[y][x] == 0):
                BFS(MAP, N, M, visited, x, y)
                cnt += 1
    return cnt

input = sys.stdin.readline

T = int(input().rstrip())
for _ in range(T):
    M, N, K = map(int, input().split())
    MAP = [[0] * M for _ in range(N)]
    for _ in range(K):
        x, y = map(int, input().split())
        MAP[y][x] = 1
    print(solution(MAP, N, M))