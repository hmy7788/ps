def solution(N, M, L):
    L.sort()

    def dfs(result):
        if len(result) == M:
            print(' '.join(map(str, result)))
            return

        for i in L:
            result.append(i)
            dfs(result)
            result.pop()

    dfs([])


N, M = map(int, input().split())
L = list(map(int, input().split()))

solution(N, M, L)