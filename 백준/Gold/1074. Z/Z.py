def solution(N, r, c):
    if N == 0: return 0
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