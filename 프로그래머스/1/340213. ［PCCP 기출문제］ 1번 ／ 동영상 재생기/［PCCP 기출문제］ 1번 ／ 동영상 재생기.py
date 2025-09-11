def to_s(m, s):
    return m * 60 + s

def to_m_s(s):
    m = s // 60
    s %= 60
    return m, s

def checking_opening(pos_s, op_start_s, op_end_s):
    if(op_start_s <= pos_s and pos_s <= op_end_s):
        return True
    return False
    
def next_cmd(video_len_s, pos_s):
    if(video_len_s - pos_s <= 10):
        return video_len_s
    return pos_s + 10

def prev_cmd(pos_s):
    if(pos_s < 10):
        return 0
    return pos_s - 10
    
def solution(video_len, pos, op_start, op_end, commands):
    video_len_s = to_s(int(video_len[0:2]), int(video_len[3:]))
    pos_s = to_s(int(pos[0:2]), int(pos[3:]))
    op_start_s = to_s(int(op_start[0:2]), int(op_start[3:]))
    op_end_s = to_s(int(op_end[0:2]), int(op_end[3:]))
    
    print(f'video_len_s: {video_len_s}')
    print(f'pos_s: {pos_s}')
    print(f'op_start_s: {op_start_s}')
    print(f'op_end_s: {op_end_s}\n')
    
    for c in commands:
        if(checking_opening(pos_s, op_start_s, op_end_s)):
            pos_s = op_end_s
        if(c == 'next'):
            pos_s = next_cmd(video_len_s, pos_s)
            if(checking_opening(pos_s, op_start_s, op_end_s)):
                pos_s = op_end_s
        else:   # c == 'prev'
            pos_s = prev_cmd(pos_s)
            if(checking_opening(pos_s, op_start_s, op_end_s)):
                pos_s = op_end_s
        print(f'command: {c}')
        print(f'pos_s: {pos_s}')
        
    m, s = map(str, to_m_s(pos_s))
    
    if(int(m) <= 9):
        m = '0' + m
    if(int(s) <= 9):
        s = '0' + s
    
    return m + ':' + s