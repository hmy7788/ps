def solution(n, lost, reserve):
    
    real_reserve = list(set(reserve) - set(lost))
    real_lost = list(set(lost) - set(reserve))
    real_lost.sort(); real_reserve.sort()
    # print(real_reserve, real_lost)
    
    for r in real_reserve:
        if r-1 in real_lost:
            real_lost.remove(r-1)
        elif r+1 in real_lost:
            real_lost.remove(r+1)
        print(real_lost)
            
    return n-len(real_lost)