X = int(input())
N = int(input())
m = 0
for _ in range(N):
    a, b = map(int, input().split())
    m += a * b
if(X == m): print('Yes')
else: print('No')