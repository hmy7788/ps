def solution(n, y, x, cnts):
    if n == 1:
        cnts[papers[y][x]+1] += 1
        return cnts

    check = True

    for i in range(y, y+n):
        if check == False:
            break

        for j in range(x, x+n):
            if papers[y][x] != papers[i][j]:
                check = False
                break
    
    if check == True:
        cnts[papers[y][x]+1] += 1
        return cnts

    new_n = n // 3

    for i in range(3):
        for j in range(3):
            solution(new_n, y+(i*new_n), x+(j*new_n), cnts)
    
    return cnts

N = int(input())
papers = [list(map(int, input().split())) for _ in range(N)] 
cnts = solution(N, 0, 0, [0, 0, 0])
print('\n'.join(map(str, cnts)))