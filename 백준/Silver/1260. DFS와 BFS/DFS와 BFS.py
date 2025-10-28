import sys
from collections import deque
sys.setrecursionlimit(10**6)
input = sys.stdin.readline

def DFS(G, visited, R, order):
    visited[R] = 1
    order.append(R)
    for n in G[R]:
        if(visited[n] == 0):
            DFS(G, visited, n, order)

def BFS(G, visited, R, order):
    visited[R] = 1
    order.append(R)
    q = deque()
    for n in G[R]:
        q.append(n)
        visited[n] = 1
        order.append(n)
    while(q):
        for n in G[q.popleft()]:
            if(visited[n] == 0):
                q.append(n)
                visited[n] = 1
                order.append(n)

N, M, V = map(int, input().split())
G = [[] for _ in range(N+1)]

for _ in range(M):
    i, j = map(int, input().split())
    G[i].append(j)
    G[j].append(i)

for g in G:
    g.sort()

visited_dfs = [0] * (N+1)
visited_bfs = [0] * (N+1)
order_dfs = []
order_bfs = []

DFS(G, visited_dfs, V, order_dfs)
print(' '.join(map(str, order_dfs)))
BFS(G, visited_bfs, V, order_bfs)
print(' '.join(map(str, order_bfs)))