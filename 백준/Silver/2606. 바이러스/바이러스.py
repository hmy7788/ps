import sys

def dfs(G, V, R):
    V[R] = 1
    for n in G[R]:
        if(V[n] == 0):
            dfs(G, V, n)

input = sys.stdin.readline
N = int(input())
M = int(input())
G = [[] for _ in range(N+2)]
V = [0] * (N+1)

for _ in range(M):
    i, j = map(int, input().split())
    G[i].append(j)
    G[j].append(i)

for g in G:
    g.sort()

dfs(G, V, 1)
print(sum(V)-1)