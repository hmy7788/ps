def solution(a, b):
    if a == b: return a
    hap = 0
    if a > b: a, b = b, a
    for i in range(a, b+1):
        hap += i
    return hap