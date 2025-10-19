matrix = []
max = -1
idx_i = 0
idx_j = 0
for _ in range(9):
    matrix.append(list(map(int, input().split())))

for i in range(9):
    for j in range(9):
        if(max < matrix[i][j]):
            max = matrix[i][j]
            idx_i = i
            idx_j = j

print(f'{max}\n{idx_i+1} {idx_j+1}')