def solution(n):
    count = 0
    for i in range(n):
        s = input()
        k = 0
        l = []
        for j in s:
            if(len(l) == 0):
                l.append(j)
            elif(j in l[:k-1]):
                if(l[-1] == j):
                    l.append(j)
                else:
                    break
            else:
                l.append(j)
            k += 1
            if(len(l) == len(s)):
                count += 1
    return count        

n = int(input())
print(solution(n))