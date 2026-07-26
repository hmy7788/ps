def solution(N, M, l):
    l.sort()

    def dfs(result):
        if len(result) == M:
            print(' '.join(map(str, result)))
            return

        for i in l:
            if i not in result:
                result.append(i)
                dfs(result)
                result.pop()

    dfs([])

N, M = map(int, input().split())
l = list(map(int, input().split()))

solution(N, M, l)