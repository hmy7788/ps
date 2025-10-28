def tile_dp(N):
    if(N == 1): return 1
    dp = [0] * (N+1)
    dp[1] = 1
    dp[2] = 2
    for i in range(3, N+1):
        dp[i] = (dp[i-1] + dp[i-2]) % 15746
    return dp[N]

print(tile_dp(int(input())))