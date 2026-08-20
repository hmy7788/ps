from collections import deque

def solution(N, K):
    dq = deque([i for i in range(1, N+1)])
    result = []
    
    while dq:
        for _ in range(K-1):
            dq.append(dq.popleft())
        result.append(dq.popleft())
    
    print('<', end='')
    print(', '.join(map(str, result)), end='')
    print('>')

N, K = map(int, input().split())
solution(N, K)