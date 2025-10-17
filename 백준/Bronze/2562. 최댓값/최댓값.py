l = []
max = -1
max_idx = -1
for i in range(9):
    n = int(input())
    if(max < n):
        max = n
        max_idx = i
print(max)
print(max_idx+1)