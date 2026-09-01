def solution(A, B):
    A.sort(); B.sort()
    i, j, win_cnt = 0, 0, 0
    
    while j <= len(B)-1:
        diff = B[j] - A[i]
        if diff > 0:
            win_cnt += 1
            i += 1
            j += 1
        elif diff <= 0:
            j += 1

    return win_cnt