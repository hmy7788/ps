def solution(s):
    answer = ''
    
    if len(s) % 2 == 0:
        return s[len(s)//2-1] + s[len(s)//2]
    else:
        return s[len(s)//2]
    
    return answer