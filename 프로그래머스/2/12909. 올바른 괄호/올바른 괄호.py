def solution(s):
    stack = []
    
    for i in s:
        if(i == '('):
            stack.append('(')
        else:
            if stack and stack.pop() == '(':
                continue
            else:
                return False
    if stack:
        return False
    return True