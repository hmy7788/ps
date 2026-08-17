def get_PPT(i, nodes, PPT, points):
    n = len(nodes)
    
    for m in range(n-1):
        sn, en = nodes[m], nodes[m+1]
        y1, x1 = points[sn-1]
        y2, x2 = points[en-1]
        
        y_step = 1 if y2 >= y1 else -1
        x_step = 1 if x2 >= x1 else -1
        
        y_range = range(y1, y2+y_step, y_step)
        x_range = range(x1+x_step, x2+x_step, x_step)
        
        for idx, dy in enumerate(y_range):
            if m > 0 and idx == 0:
                continue
            PPT[i].append((dy, x1))
            
        for dx in x_range:
            PPT[i].append((y2, dx))        
        
    return PPT
                

def solution(points, routes):
    cnt = 0
    N = len(routes)
    PPT = [[] for _ in range(N)]
    
    for i, nodes in enumerate(routes):
        PPT = get_PPT(i, nodes, PPT, points)
    
    max_t = max(len(p) for p in PPT)
    
    # for p in PPT:
    #     print(p)
        
    for t in range(max_t):
        d = {}
        for r in range(N):
            if len(PPT[r]) <= t:
                continue
            
            if PPT[r][t] in d:
                d[PPT[r][t]] += 1
            else:
                d[PPT[r][t]] = 1
        
        for v in d.values():
            if v > 1:
                cnt += 1
                
    return cnt