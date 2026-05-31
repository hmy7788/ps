def solution(s):
    flag = False
    if(len(s) == 4 or len(s) == 6):
        for i in s:
            if(i.isalpha()):
                return False
        return True
    return False