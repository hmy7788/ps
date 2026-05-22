def solution(prices):
    answer = []
    n = len(prices)
    
    for i in range(n):
        for j in range(i+1, n):
            p, q = prices[i], prices[j]
            if p > q or j == n-1:
                answer.append(j-i)
                break
    print(answer.append(0))
    
    return answer