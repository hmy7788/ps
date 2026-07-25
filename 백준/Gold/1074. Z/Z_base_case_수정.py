def solution(N, r, c):
    if N == 1:
        if r == 0 and c == 0: return 0
        if r == 0 and c == 1: return 1
        if r == 1 and c == 0: return 2
        else: return 3
        
    half = 2**(N-1)

    # r과 c가 1번 사각형일때
    if r < half and c < half: return solution(N-1, r, c)

    # r과 c가 2번 사각형일때
    if r < half and c >= half: return half*half + solution(N-1, r, c-half)

    # r과 c가 3번 사각형일때
    if r >= half and c < half: return 2*half*half + solution(N-1, r-half, c)
    
    # r과 c가 4번 사각형일때
    return 3*half*half + solution(N-1, r-half, c-half)

N, r, c = map(int, input().split())
print(solution(N, r, c))