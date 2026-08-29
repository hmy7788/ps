def solution(n):    
    def get_marking_board(y, x, marking):
        delta = 1 if marking else -1
        
        for i in range(y): board[i][x] += delta # 상
        for i in range(y+1, n): board[i][x] += delta # 하
        for i in range(x): board[y][i] += delta # 좌
        for i in range(x+1, n): board[y][i] += delta # 우
        
        i, j = y-1, x-1
        while i >= 0 and j >= 0: # 좌상 대각
            board[i][j] += delta
            i -= 1; j -= 1;
        i, j = y-1, x+1
        while i >= 0 and j < n: # 우상 대각
            board[i][j] += delta
            i -= 1; j += 1
        i, j = y+1, x-1
        while i < n and j >= 0: # 좌하 대각
            board[i][j] += delta
            i += 1; j -= 1
        i, j = y+1, x+1
        while i < n and j < n: # 우하 대각
            board[i][j] += delta
            i += 1; j += 1
        
        
    def DFS(y, x):
        if y == n-1: return 1
        
        total = 0
        for nx, value in enumerate(board[y+1]):
            if value == 0:
                board[y+1][nx] = 1
                get_marking_board(y+1, nx, True)
                total += DFS(y+1, nx)
                board[y+1][nx] = 0
                get_marking_board(y+1, nx, False)
        
        return total
    
    
    m = (n//2)-1 if n%2 == 0 else n//2
    result = []
    
    for x in range(m+1):
        board = [[0 for _ in range(n)] for _ in range(n)]
        board[0][x] = 1
        get_marking_board(0, x, True)
        total = DFS(0, x)
        result.append(total)
        
    print(result)
    return 2*sum(result) if n%2 == 0 else 2*sum(result[:m]) + result[m]