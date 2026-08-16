def solution(board, moves):
    stack = []
    cnt = 0
    n = len(board)
    
    for m in moves:
        for y in range(n):
            x = m-1
            if board[y][x] != 0 or y == n-1:
                break
            
        selected = board[y][x]
        board[y][x] = 0
        
        if stack and selected != 0:
            if stack[-1] == selected:
                cnt += 2
                stack.pop()
            else:
                stack.append(selected)
        else:
            stack.append(selected)
        
    return cnt