import sys
sys.setrecursionlimit(10**6)

alphabets = 'AEIOU'

def solution(word):
    s = ''
    d = []
    
    def dfs(w):
        if w != '':
            d.append(w)
        if len(w) == 5:
            return
        
        for s in alphabets:
            dfs(w+s)
            
    dfs('')
    
    return d.index(word)+1