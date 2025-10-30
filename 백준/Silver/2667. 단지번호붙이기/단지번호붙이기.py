import sys
from collections import deque

def bfs(n,m,v,i,j,r):
    q = deque()
    v[i][j] = 1
    q.append([i,j])
    c = 1
    while(q):
        cp = q.popleft()
        ci, cj = cp[0], cp[1]
        for di, dj in ((-1,0),(0,-1),(1,0),(0,1)):
            ni, nj = ci + di, cj + dj
            if((0 <= ni < n) and (0 <= nj < n) and (m[ni][nj] == 1) and (v[ni][nj] == 0)):
                q.append([ni, nj])
                v[ni][nj] = 1
                c += 1
    r.append(c)

def solution(n):
    m = []
    r = []
    v = [[0]*n for _ in range(n)]
    for _ in range(n):
        m.append(list(map(int, sys.stdin.readline().strip())))
    for i in range(n):
        for j in range(n):
            if(m[i][j] == 1 and v[i][j] == 0):
                bfs(n,m,v,i,j,r)
    r.sort()
    print(len(r))
    print('\n'.join(map(str,r)))

n = int(sys.stdin.readline())
solution(n)