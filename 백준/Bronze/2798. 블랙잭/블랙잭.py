def solution(n,m):
    l = list(map(int,input().split()))
    max = -1
    for i in range(n):
        for j in range(i+1,n):
            for k in range(j+1,n):
                sum = l[i]+l[j]+l[k]
                if(sum > max and sum <= m):
                    max = sum
    print(max)

n,m = map(int, input().split())
solution(n,m)