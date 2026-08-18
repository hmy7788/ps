def solution(n, w, num):
    floor = n//w+1 if n%w else n//w
    boxs = [[0 for _ in range(w)] for _ in range(floor)]
    cnt, i = 0, 1
    cy, cx = 0, 0
    
    for y in range(floor):
        x_range = range(w)
        if y % 2 != 0:
            x_range = range(w-1, -1, -1)
        
        for x in x_range:
            if num == i:
                cy, cx = y, x
            if i == n+1:
                break
            
            boxs[y][x] = i
            i += 1
    
    while 0 <= cy < floor and boxs[cy][cx] != 0:
        cnt += 1
        cy += 1
        
    return cnt