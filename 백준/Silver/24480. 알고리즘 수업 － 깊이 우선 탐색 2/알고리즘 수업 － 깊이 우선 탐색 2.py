import sys
sys.setrecursionlimit(10**6)

def dfs(G, R, visited):
    global count
    visited[R] = count
    count += 1
    for nv in G[R]:
        if(visited[nv] == 0):
            dfs(G, nv, visited)

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
    G[i].sort(reverse=True)

dfs(G, R, visited)
print('\n'.join(map(str, visited[1:])))