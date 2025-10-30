from collections import deque
import sys

def BFS(N, K):
    q = deque()
    q.append([N, 0])
    visited = [0] * ((10**5)+1)
    visited[N] = 1

    while(q):
        current_point = q.popleft()
        current_N, current_sec = current_point[0], current_point[1]
        
        if(current_N == K): return current_sec

        for next_N in [current_N-1, current_N+1, 2*current_N]:
            if(0 <= next_N <= 10**5 and visited[next_N] == 0):
                q.append([next_N, current_sec+1])
                visited[next_N] = 1

input = sys.stdin.readline
N, K = map(int, input().split())
print(BFS(N, K))