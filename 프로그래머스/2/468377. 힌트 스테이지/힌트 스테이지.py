def solution(cost, hint):
    n = len(cost)
    answer = float('inf')
    
    for bitmask in range(2**(n-1)):
        ticket_cost = 0
        hint_cost = 0
        hint_count = [0] * n
        
        for i in range(n-1):
            if bitmask & (1 << i):
                hint_cost += hint[i][0]
                for h in hint[i][1:]:
                    hint_count[h-1] += 1
        
        # print(hint_cost, hint_count)
        
        for i, hc in enumerate(hint_count):
            used = min(hc, n-1)
            ticket_cost += cost[i][used]
        
        if ticket_cost + hint_cost < answer:
            answer = ticket_cost + hint_cost

    return answer