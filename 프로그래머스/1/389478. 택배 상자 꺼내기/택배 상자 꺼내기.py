def solution(n, w, num):
    floor = n // w + 1
    boxs = [[0]*w for _ in range(floor)]
    value = 1
    
    for i in range(floor):
        if(i % 2 == 0): # 순방향
            for j in range(w):
                if(value == n+1): break
                boxs[i][j] = value
                value += 1
        else: # 역방향
            for j in range(w-1, -1, -1):
                if(value == n+1): break
                boxs[i][j] = value
                value += 1
    
    ci, cj = 0, 0
    for i in range(floor):
        for j in range(w):
            if(boxs[i][j] == num):
                ci, cj = i, j
                break
                
    if(boxs[floor-1][cj] == 0):
        return floor-2 - ci + 1
    else:
        return floor-1 - ci + 1
    
    
        
        
    print(boxs)
    