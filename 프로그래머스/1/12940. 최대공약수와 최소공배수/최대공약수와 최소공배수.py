def GCD(n, m):
    if m == 0: return n
    return GCD(m, n%m)

def solution(n, m):
    if n < m: n, m = m, n
    gcd = GCD(n, m)
    return [gcd, (n*m)/gcd]
