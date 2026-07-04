def solution(clothes):
    d = {}
    
    for i in clothes:
        cloth_name, cloth_kind = i[0], i[1]
        if cloth_kind in d:
            d[cloth_kind] += 1
        else:
            d[cloth_kind] = 1
            
    cnt = 1
    
    for v in d.values():
        cnt *= (v+1)
    
    return cnt-1