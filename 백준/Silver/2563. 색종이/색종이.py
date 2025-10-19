def solution(n):
    map_size = [[0 for i in range(100)] for j in range(100)]
    area = 0

    for i in range(n):
        x,y = map(int,input().split())
        for j in range(x,x+10):
            for k in range(y,y+10):
                map_size[k][j] = 1
    
    for i in range(100):
        for j in range(100):
            if(map_size[i][j] == 1):
                area += 1
    
    print(area)
            

solution(int(input()))