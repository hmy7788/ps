results = []

def solution(N, M):
    def dfs(lst):
        if len(lst) == M:
            results.append(lst[:])
            return
        
        for i in range(1, N+1):
            if i not in lst:
                lst.append(i)
                dfs(lst)
                lst.pop()

    dfs([])

    for i in results:
        print(' '.join(map(str, i)))

N, M = map(int, input().split())
solution(N, M)