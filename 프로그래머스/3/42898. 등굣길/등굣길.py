def solution(m, n, puddles):
    dp = [[0 for _ in range(m)] for _ in range(n)]
    dp[0][0] = 1
    
    for p in puddles:
        px, py = p[0], p[1]
        dp[py-1][px-1] = -1
        
    for y in range(n):
        for x in range(m):
            if dp[y][x] == -1: continue
            
            if 0 <= x-1 < m and dp[y][x-1] != -1:
                dp[y][x] += dp[y][x-1]
            if 0 <= y-1 < n and dp[y-1][x] != -1:
                dp[y][x] += dp[y-1][x]
    
    return dp[n-1][m-1] % 1000000007