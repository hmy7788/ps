matrix = [['' for _ in range(15)] for _ in range(5)]
result = ''

for i in range(5):
    s = input()
    for j in range(len(s)):
        matrix[i][j] = s[j]

for i in range(15):
    for j in range(5):
        if(matrix[j][i] != ''):
            result += matrix[j][i]

print(result)