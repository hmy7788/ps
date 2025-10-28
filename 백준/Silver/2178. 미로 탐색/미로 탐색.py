import sys
from collections import deque

def bfs(n,m,map_list):
    q = deque()
    v = [[0]*m for _ in range(n)]
    q.append([0,0])
    v[0][0] = 1
    while(q):
        cp = q.popleft()
        ci, cj = cp[0], cp[1]
        for di, dj in ((-1,0), (1,0), (0,-1), (0,1)):
            ni, nj = ci + di, cj + dj
            if((0 <= ni < n) and (0 <= nj < m) and (map_list[ni][nj] == 1) and (v[ni][nj] == 0)):
                q.append([ni,nj])
                v[ni][nj] = v[ci][cj] + 1
    print(v[n-1][m-1])

def solution(n,m):
    map_list = []
    for _ in range(n):
        map_list.append(list(map(int,sys.stdin.readline().strip())))
    bfs(n,m,map_list)
    
n,m = map(int,sys.stdin.readline().split())
solution(n,m)