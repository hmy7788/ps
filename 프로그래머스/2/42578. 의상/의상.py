def solution(clothes):
    d = {}
    
    for i in clothes:
        cloth_name, cloth_kind = i[0], i[1]
        if cloth_kind in d.keys():
            d[cloth_kind].append(cloth_name)
        else:
            d[cloth_kind] = [cloth_name]
            
    print(d)
    cnt = 1
    
    for k, v in d.items():
        cnt *= len(v) + 1
    return cnt-1