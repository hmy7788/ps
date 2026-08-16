def solution(a, b):
    dp = 0
    
    for i, j in zip(a, b):
        dp += i*j
        
    return dp