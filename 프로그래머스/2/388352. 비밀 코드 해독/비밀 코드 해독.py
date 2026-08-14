def solution(n, q, ans):
    v = [0 for _ in range(n+1)]
    cand_cnt = 0
    
    def dfs(result):
        nonlocal cand_cnt
        if len(result) == 5:
            # print(' '.join(map(str, result)))
            
            for l, a in zip(q, ans):
                count = 0
                for i in result:
                    for j in l:
                        if i == j: count += 1
                if a != count: return
                
            cand_cnt += 1
            return
        
        for i in range(1, n+1):
            if (len(result) == 0 or result[-1] < i) and v[i] == 0:
                v[i] = 1
                result.append(i)
                dfs(result)
                v[i] = 0
                result.pop()
    
    dfs([])
    return cand_cnt