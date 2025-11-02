import sys

input = sys.stdin.readline
a0, a1 = map(int, input().split())
c = int(input())
n0 = int(input())
flag = True

for n in range(n0, 1000000):
    f = a0 * n + a1
    g = n
    if(f <= c * g): flag = True
    else: flag = False; break
if(flag): print(1)
else: print(0)