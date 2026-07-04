from collections import defaultdict

def solution(tickets):
    g = defaultdict(list)
    for s, e in tickets:
        g[s].append(e)
    
    for v in g.values():
        v.sort()
    
    def dfs(current, path):
        if len(path) == len(tickets)+1:
            return path
        
        if current in g:
            for i in range(len(g[current])):
                next_dst = g[current].pop(i)
                path.append(next_dst)
                result = dfs(next_dst, path)
                
                if result:
                    return result
                
                path.pop()
                g[current].insert(i, next_dst)
        
        return False
    
    return dfs("ICN", ["ICN"])