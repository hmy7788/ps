def solution(s, n):
    cp = ''
    
    for i in s:
        if i.isupper():
            cp += chr((ord(i) - ord('A') + n) % 26 + ord('A'))
        elif i.islower():
            cp += chr((ord(i) - ord('a') + n) % 26 + ord('a'))
        else:
            cp += ' '
    
    return cp