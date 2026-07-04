alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def change_alphabet(target_alpha):
    idx = alpha.index(target_alpha)
    print(idx)
    
    if idx <= 13:
        return idx
    elif idx >= 14:
        return 26-idx


def solution(name):
    n = len(name)
    
    up_down_cnt = 0
    for ch in name:
        idx = ord(ch) - ord('A')
        up_down_cnt += min(idx, 26-idx)
    
    min_move = n-1
    
    for i in range(n):
        next_i = i+1
        while next_i < n and name[next_i] == 'A':
            next_i += 1
        
        path2 = i+i+(n-next_i)
        path3 = (n-next_i) + (n-next_i) + i
        
        min_move = min(min_move, path2, path3)
    
    return up_down_cnt + min_move
        
    
    return cnt