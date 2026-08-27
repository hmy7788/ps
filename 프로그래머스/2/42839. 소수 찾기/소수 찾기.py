def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n**(1/2))+1):
        if n % i == 0:
            return False
    return True

def get_comb(numbers):
    n = len(numbers)
    v = [0] * n
    comb = set()
    
    def DFS(current_str):
        if len(current_str) == n:
            comb.add(int(current_str))
            return
        for i, s in enumerate(numbers):
            if v[i] == 0:
                comb.add(int(current_str+s))
                v[i] = 1
                DFS(current_str+s)
                v[i] = 0
    DFS('')
    return comb

def solution(numbers):
    comb = get_comb(numbers)
    cnt = 0
    
    for c in comb:
        if is_prime(c): cnt += 1
    
    return cnt