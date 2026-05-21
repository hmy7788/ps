def solution(numbers):
    n, m = len(numbers), float('-inf')
    
    for i in range(n):
        for j in range(i+1, n):
            num = numbers[i] * numbers[j]
            if m < num:
                m = num
    
    return m