def solution(absolutes, signs):
    hap = 0
    
    for a, s in zip(absolutes, signs):
        if s:
            hap += a
        else:
            hap -= a
            
    return hap