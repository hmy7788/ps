def solution(points, routes):
    cnt = 0
    N = len(routes)
    PPT = [[] for _ in range(N)]
    max_t = -1
    
    for i, node in enumerate(routes):
        sn, en = node[0], node[1]
        sn_point = points[sn-1]
        en_point = points[en-1]
        
        y1, x1 = sn_point[0], sn_point[1]
        y2, x2 = en_point[0], en_point[1]
        
        # 하우
        if y2 >= y1 and x2 >= x1:
            for y in range(y1, y2+1):
                PPT[i].append((y, x1))
            for x in range(x1+1, x2+1):
                PPT[i].append((y2, x))
        
        # 하좌
        elif y2 >= y1 and x2 <= x1:
            for y in range(y1, y2+1):
                PPT[i].append((y, x1))
            for x in range(x1+1, x2-1, -1):
                PPT[i].append((y2, x))
        
        # 상우
        elif y2 <= y1 and x2 >= x1:
            for y in range(y1, y2-1, -1):
                PPT[i].append((y, x1))
            for x in range(x1+1, x2+1):
                PPT[i].append((y2, x))
        
        # 상좌
        elif y2 <= y1 and x2 <= x1:
            for y in range(y1, y2-1, -1):
                PPT[i].append((y, x1))
            for x in range(x1+1, x2-1, -1):
                PPT[i].append((y2, x))
        
        if len(PPT[i]) > max_t:
            max_t = len(PPT[i])
            
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