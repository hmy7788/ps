N = int(input())
score = list(map(int, input().split()))
sum = 0
max_score = max(score)
for s in score:
    sum += s / max_score * 100
print(sum/N)