def solution(info, n, m):
    info.sort(key=lambda x: x[0]-x[1], reverse=True)
    A_cnt = 0
    
    for A, B in info:
        if m > B:
            m -= B
            continue
        elif n > A:
            n -= A
            A_cnt += A
            continue
        else:
            return -1
        
    return A_cnt