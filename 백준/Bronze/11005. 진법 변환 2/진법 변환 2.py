def solution(n,m):
    result = ''
    alpha_list = [chr(i) for i in range(65,91)]
    quotient = n
    remainder = m
    l = []
    while(quotient >= remainder):
        l.append(quotient % remainder)
        quotient //= remainder
    l.append(quotient)
    l.reverse()
    for i in l:
        if(i >= 10):
            result += alpha_list[i-10]
        else:
            result += str(i)
    print(result)

n,m = map(int,input().split())
solution(n,m)