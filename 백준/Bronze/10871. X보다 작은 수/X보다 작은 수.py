N, X = map(int, input().split())
l = list(map(int, input().split()))
for i in l:
    if(i < X):
        print(i, end=' ')