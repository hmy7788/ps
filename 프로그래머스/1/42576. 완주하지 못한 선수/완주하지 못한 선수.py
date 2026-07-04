def solution(p, c):
    p_dict = {}
    for name in p:
        if(name in p_dict):
            p_dict[name] += 1
        else:
            p_dict[name] = 1
            
    for name in c:
        p_dict[name] -= 1
    
    for name in p_dict:
        if(p_dict[name] > 0):
            return name