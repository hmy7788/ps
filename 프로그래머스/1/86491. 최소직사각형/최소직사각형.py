def solution(sizes):
    w = []
    h = []
    
    for i in sizes:
        w.append(max(i))
        h.append(min(i))
    
    return max(w) * max(h)