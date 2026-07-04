def solution(cards):
    cards = [-1] + cards
    v = [-1 for _ in range(len(cards))]
    groups = []

    def dfs(current):
        if v[current] != -1:
            groups.append(g)
            return
        
        g.append(cards[current])
        next = cards[current]
        v[current] = 1
        dfs(next)

    for i in range(1, len(cards)):
        if v[i] == -1:
            g = []
            dfs(i)
    
    groups.sort(key=lambda x:len(x))

    if len(groups) == 1: return 0
    return len(groups[-1]) * len(groups[-2])