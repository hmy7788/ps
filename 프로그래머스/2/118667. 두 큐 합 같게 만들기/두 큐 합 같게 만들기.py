from collections import deque

def solution(queue1, queue2):
    dq1, dq2, n = deque(queue1), deque(queue2), len(queue1)
    s1, s2 = sum(dq1), sum(dq2)
    target_number = int((s1 + s2) // 2)
    cnt = 0
    
    if (s1 + s2) % 2 != 0: return -1
    
    while cnt <= 3*n:
        if s1 == target_number:
            break
        if dq1[0] > target_number or dq2[0] > target_number:
            return -1
        if s1 < s2:
            v2 = dq2.popleft()
            dq1.append(v2)
            s1 += v2
            s2 -= v2
        else:
            v1 = dq1.popleft()
            dq2.append(v1)
            s1 -= v1
            s2 += v1
        cnt += 1
    else:
        return -1
        
    return cnt