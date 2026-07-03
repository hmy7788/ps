import sys

input = sys.stdin.readline
s = input().strip()
n = len(s)
d = []

for i in range(n-1):
    for j in range(i+1, n-1):
        s1 = s[:i+1]
        s2 = s[i+1:j+1]
        s3 = s[j+1:]
        d.append(s1[::-1]+s2[::-1]+s3[::-1])

d.sort()
print(d[0])