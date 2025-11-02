import sys

def brute_force(n, arr):
    max_value = arr[0]
    for i in range(1, n+1):
        for j in range(n-i+1):
            sum_value = sum(arr[j:i+j])
            if(max_value < sum_value):
                max_value = sum_value
    return max_value

def dp(n, arr):
    dp = [0] * n
    dp[0] = arr[0]
    max_value = arr[0]
    for i in range(1, n):
        dp[i] = max(arr[i], arr[i]+dp[i-1])
        if(max_value < dp[i]): max_value = dp[i]
    return max_value

input = sys.stdin.readline
n = int(input())
arr = list(map(int, input().split()))

print(dp(n, arr))