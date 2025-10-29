N, K = map(int, input().split())
coins = []
cnt = 0

for _ in range(N):
    coins.append(int(input()))

for i in range(N-1, -1, -1):
    c = coins[i]
    cnt += (K // c)
    K %= c

print(cnt)