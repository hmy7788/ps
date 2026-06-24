def is_prime(n):
    if n < 2: return False
        
    for i in range(2, int(n**(1/2))+1):
        if n % i == 0:
            return False
        
    return True    


def solution(numbers):
    n = len(numbers)
    order = set()
    v = [0] * n
    
    def make_permutation(current_str):
        if len(current_str) == n:
            order.add(int(current_str))
            return
        
        for i in range(n):
            if v[i] == 0:
                order.add(int(current_str+numbers[i]))
                v[i] = 1
                make_permutation(current_str+numbers[i])
                v[i] = 0
    
    make_permutation('')
    cnt = 0
    
    for n in order:
        if is_prime(n): cnt += 1
    
    return cnt