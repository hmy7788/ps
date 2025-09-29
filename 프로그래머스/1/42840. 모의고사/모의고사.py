def make_math1(n):
    math1 = [1,2,3,4,5]
    math1 = math1 * ((n//5)+1)
    return math1[:n]

def make_math2(n):
    math2 = [2,1,2,3,2,4,2,5]
    math2 = math2 * ((n//8)+1)
    return math2[:n]

def make_math3(n):
    math3 = [3,3,1,1,2,2,4,4,5,5]
    math3 = math3 * ((n//10)+1)
    return math3[:n]
    
def solution(answers):
    n = len(answers)
    math1 = make_math1(n)
    math2 = make_math2(n)
    math3 = make_math3(n)
    counting = [0, 0, 0]
    answer = []
    
    for i in range(n):
        if(math1[i] == answers[i]): counting[0] += 1
        if(math2[i] == answers[i]): counting[1] += 1
        if(math3[i] == answers[i]): counting[2] += 1
        
    print(counting)
    hs = max(counting)
    
    for i in range(3):
        if(max(counting) == counting[i]):
            answer.append(i+1)
        
    print(math1)
    print(math2)
    print(math3)
    return answer