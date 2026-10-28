def solution(elements):
    n = len(elements)
    elements *= 2
    result = set()
    
    for length in range(1, n+1):
        for i in range(n):
            result.add(sum(elements[i : i+length]))
    
    return len(result)