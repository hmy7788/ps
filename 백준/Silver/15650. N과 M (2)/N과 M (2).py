def solution(N, M):
    def dfs(lst):
        if len(lst) == M:
            print(' '.join(map(str, lst)))
            return

        for i in range(1, N+1):
            if i not in lst and (len(lst) == 0 or lst[-1] < i):
                lst.append(i)
                dfs(lst)
                lst.pop()

    dfs([])

N, M = map(int, input().split())
solution(N, M)