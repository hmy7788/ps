from collections import deque

def solution(number, k):
    stack = []
    i = k
    
    for num in number:
        while k > 0 and stack and int(stack[-1]) < int(num):
            stack.pop()
            k -= 1
        
        stack.append(num)
        
    if k == 0:
        return ''.join(stack)
    else:
        return ''.join(stack[:k+1])