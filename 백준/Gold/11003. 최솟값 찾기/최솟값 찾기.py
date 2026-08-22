from collections import deque

def solution(N, L, arr):
    dq = deque()
    result = []

    for i, a in enumerate(arr):
        while dq and arr[dq[-1]] >= a:
            dq.pop()

        dq.append(i)

        while dq[0] <= i-L:
            dq.popleft()
    
        result.append(arr[dq[0]])

    print(' '.join(map(str, result)))

N, L = map(int, input().split())
arr = list(map(int, input().split()))
solution(N, L, arr)