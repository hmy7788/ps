def solution(targets):
    targets.sort(key=lambda x:x[1])
    
    last = float('-inf')
    cnt = 0
    
    for s, e in targets:
        if s >= last:
            last = e
            cnt += 1
    
    return cnt