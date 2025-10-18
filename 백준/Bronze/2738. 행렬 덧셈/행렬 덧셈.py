N, M = map(int, input().split())
matrix_A = []
matrix_B = []

for _ in range(N):
    matrix_A.append(list(map(int, input().split())))

for _ in range(N):
    matrix_B.append(list(map(int, input().split())))

for row in range(N):
    for col in range(M):
        print(matrix_A[row][col] + matrix_B[row][col], end=' ')
    print()