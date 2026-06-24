order = []

def make_permutation(perm, n):
    if len(perm) == n:
        order.append(perm[:])
        return
    
    for i in range(n):
        if v[i] == 0:
            perm.append(i)
            v[i] = 1
            make_permutation(perm, n)
            perm.pop()
            v[i] = 0

def solution(k, dungeons):
    n = len(dungeons)
    order = []
    v = [0] * n
    
    def make_permutation(perm):
        if len(perm) == n:
            order.append(perm[:])
            return
        
        for i in range(n):
            if v[i] == 0:
                perm.append(i)
                v[i] = 1
                make_permutation(perm)
                perm.pop()
                v[i] = 0
    
    max_cnt = float('-inf')
    make_permutation([])
    
    for p in order:
        current_piro = k
        cnt = 0
        
        for idx in p:
            need_piro = dungeons[idx][0]
            consume_piro = dungeons[idx][1]
            
            if current_piro >= need_piro:
                current_piro -= consume_piro
                cnt += 1
            else:
                break
        
        if max_cnt < cnt:
            max_cnt = cnt
            
    return max_cnt
    
    return max_cnt