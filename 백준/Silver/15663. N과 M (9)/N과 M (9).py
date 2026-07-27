def solution(N, M, L):
    L.sort()
    v = [0 for _ in range(N)]

    def dfs(result):
        if len(result) == M:
            print(' '.join(map(str, result)))
            return

        for i in range(len(L)):
            if v[i] == 1:
                continue
            if i > 0 and L[i-1] == L[i] and v[i-1] == 0:
                continue
    
            result.append(L[i])
            v[i] = 1
            dfs(result)
            result.pop()
            v[i] = 0
            
    dfs([])

N, M = map(int, input().split())
L = list(map(int, input().split()))

solution(N, M, L)