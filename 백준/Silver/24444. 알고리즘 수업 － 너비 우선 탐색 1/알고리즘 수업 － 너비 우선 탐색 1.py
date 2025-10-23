import sys
from collections import deque 

def bfs(G, R, visited):
    count = 1
    visited[R] = count
    q = deque()
    for nv in G[R]:
        q.append(nv)
    while(q):
        u = q.popleft()
        if(visited[u] == 0):
            count += 1
            visited[u] = count
            for nv in G[u]:
                q.append(nv)
    return visited

input = sys.stdin.readline
N, M, R = map(int, input().split())
G = [[] for _ in range(N+1)]
visited = [0] * (N+1)
count = 1

for _ in range(M):
    i, j = map(int, input().split())
    G[i].append(j)
    G[j].append(i)

for i in range(1, N+1):
    G[i].sort()

visited = bfs(G, R, visited)
print('\n'.join(map(str, visited[1:])))