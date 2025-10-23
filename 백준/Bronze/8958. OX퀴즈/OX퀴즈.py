T = int(input())

for _ in range(T):
    score = 0
    sum = 1
    answer = input()
    for a in answer:
        if(a == 'O'):
            score += sum
            sum += 1
        else:
            sum = 1
    print(score)