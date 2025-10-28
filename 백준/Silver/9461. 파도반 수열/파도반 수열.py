def P(N):
    dp = [0, 1, 1, 1, 2, 2]
    for i in range(6, N+1):
        dp.append(dp[i-1] + dp[i-5]) 
    return dp[N]

T = int(input())
for _ in range(T):
    N = int(input())
    print(P(N))