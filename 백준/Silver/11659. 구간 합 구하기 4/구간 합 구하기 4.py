import sys
input = sys.stdin.readline

def solution(n,m):
    l = list(map(int,input().split()))
    prefix_sum_list = [0]
    sum = 0

    for i in l:
        sum += i
        prefix_sum_list.append(sum)

    for i in range(m):
        left,right = map(int,input().split())
        print(prefix_sum_list[right] - prefix_sum_list[left-1])

n,m = map(int, input().split())
solution(n,m)