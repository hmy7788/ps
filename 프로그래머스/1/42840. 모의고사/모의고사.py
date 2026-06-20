def solution(answers):
    math1 = [1,2,3,4,5]
    math2 = [2,1,2,3,2,4,2,5]
    math3 = [3,3,1,1,2,2,4,4,5,5]
    
    scores = [0, 0, 0]
    
    for i in range(len(answers)):
        if answers[i] == math1[i%5]: scores[0] += 1
        if answers[i] == math2[i%8]: scores[1] += 1
        if answers[i] == math3[i%10]: scores[2] += 1
    
    max_score = max(scores)
    result = []
    
    for i in range(3):
        if max_score == scores[i]:
            result.append(i+1)
            
    return result
