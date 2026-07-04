from collections import deque

def can_exit(maps, i, j):
    dq = deque()
    dq.append((i, j))
    y, x = len(maps), len(maps[0])
    v = [[False for _ in range(x)] for _ in range(y)]
    v[i][j] = True
    
    while dq:
        cy, cx = dq.popleft()
        for dy, dx in [(0, -1), (-1, 0), (0, 1), (1, 0)]:
            ny, nx = cy+dy, cx+dx
            if 0 <= ny < y and 0 <= nx < x:
                if maps[ny][nx] == '1' and v[ny][nx] == False:
                    dq.append((ny, nx))
                    v[ny][nx] = True
            else:
                 return True
    
    return False

def solution(storage, requests):
    y, x = len(storage), len(storage[0])
    map_size = y * x
    maps = list(map(list, storage))
    
    for req in requests:
        if len(req) == 1:
            alpha = req[0]
            cnt = 0
            exit_points = []
            for i in range(y):
                for j in range(x):
                    if maps[i][j] == alpha and can_exit(maps, i, j):
                        exit_points.append((i, j))
                        cnt += 1
            
            for ep in exit_points:
                exit_point_y, exit_point_x = ep
                maps[exit_point_y][exit_point_x] = '1'
                
            map_size -= cnt
            
        else:
            alpha = req[0]
            cnt = 0
            for i in range(y):
                for j in range(x):
                    if maps[i][j] == alpha:
                        maps[i][j] = '1'
                        cnt += 1
            map_size -= cnt
    
        # print(maps)
        
    return map_size