def is_win(board):
    O_win, X_win = False, False
    
    # 가로
    for i in range(3):
        if board[i][0] == 'O' and board[i][1] == 'O' and board[i][2] == 'O':
            O_win = True
        if board[i][0] == 'X' and board[i][1] == 'X' and board[i][2] == 'X':
            X_win = True
    
    # 세로
    for i in range(3):
        if board[0][i] == 'O' and board[1][i] == 'O' and board[2][i] == 'O':
            O_win = True
        if board[0][i] == 'X' and board[1][i] == 'X' and board[2][i] == 'X':
            X_win = True
            
    # 대각1
    if board[0][0] == 'O' and board[1][1] == 'O' and board[2][2] == 'O':
        O_win = True
    if board[0][0] == 'X' and board[1][1] == 'X' and board[2][2] == 'X':
        X_win = True
    
    # 대각2
    if board[0][2] == 'O' and board[1][1] == 'O' and board[2][0] == 'O':
        O_win = True
    if board[0][2] == 'X' and board[1][1] == 'X' and board[2][0] == 'X':
        X_win = True
        
    return O_win, X_win


def solution(board):
    O_count, X_count = 0, 0
    
    for i in range(3):
        for j in range(3):
            if board[i][j] == 'O':
                O_count += 1
            elif board[i][j] == 'X':
                X_count += 1
    
    O_win, X_win = is_win(board)
         
    if X_count > O_count or O_count > X_count + 1:
        return 0
    
    if O_win and O_count != X_count + 1:
        return 0
    
    if X_win and O_count != X_count:
        return 0
    
    return 1