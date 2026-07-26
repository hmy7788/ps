def solution(N, M):
    def dfs(l):
        if len(l) == M:
            print(' '.join(map(str, l)))
            return
        
        for i in range(1, N+1):
            l.append(i)
            dfs(l)
            l.pop()

    dfs([])


N, M = map(int, input().split())
solution(N, M)