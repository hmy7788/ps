def binary_search(target, l1, result: list):
    start = 0
    end = len(l1)-1

    while(start <= end):
        mid = (end+start)//2
        if(l1[mid] == target):
            result.append(1)
            return
        elif(l1[mid] < target):
            start = mid + 1
        else:
            end = mid - 1
    result.append(0)

def solution(l1: list, l2: list):
    result = []
    l1.sort()
    for target in l2:
        binary_search(target, l1, result)
        
    print('\n'.join(map(str,result)))

n = int(input())
l1 = list(map(int,input().split()))
m = int(input())
l2 = list(map(int,input().split()))
solution(l1,l2)