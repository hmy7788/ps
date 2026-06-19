def solution(cards):
    n = len(cards)
    groups = []
    v = [0] * n
    
    for i in range(n):
        if v[i] == 0:   # 방문 안했을때
            count = 0
            curr = i
            
            while v[curr] == 0: 
                v[curr] = 1
                curr = cards[curr]-1
                count += 1
                
            groups.append(count)
    
    if len(groups) == 1:
        return 0
    else:
        groups.sort()
        return groups[-1] * groups[-2]