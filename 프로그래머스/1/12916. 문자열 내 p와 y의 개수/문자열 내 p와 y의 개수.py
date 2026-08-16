def solution(s):
    pcnt = 0
    ycnt = 0
    
    for i in s:
        if i == 'p' or i == 'P':
            pcnt += 1
        elif i == 'y' or i == 'Y':
            ycnt += 1
    
    if pcnt == 0 and ycnt == 0: return True
    elif pcnt == ycnt: return True
    else: return False