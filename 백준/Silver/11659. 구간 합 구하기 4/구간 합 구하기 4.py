import sys
input = sys.stdin.readline

N, M = map(int, input().split())
l = list(map(int, input().split()))
p = [0 for _ in range(len(l)+1)]

for i in range(1, len(p)):
    p[i] = l[i-1] + p[i-1]

for _ in range(M):
    i, j = map(int, input().split())
    print(p[j] - p[i-1])
