def solution(arr1, arr2):
    row1, col1 = len(arr1), len(arr1[0])
    row2, col2 = len(arr2), len(arr2[0])
    answer = [[0] * col2 for _ in range(row1)]
    
    for i in range(row1):
        for j in range(col2):
            s = 0
            for k in range(col1):
                s += arr1[i][k] * arr2[k][j]
            answer[i][j] = s
            
    return answer