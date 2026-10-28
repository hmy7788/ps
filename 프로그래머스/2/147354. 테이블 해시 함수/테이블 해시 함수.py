def solution(data, col, row_begin, row_end):
    answer = 0
    data.sort(key=lambda x : (x[col-1], -x[0]))
    
    for i in range(row_begin-1, row_end):
        row = data[i]
        S_i = 0
        for v in row:
            S_i += v % (i+1)
        answer ^= S_i
        
    return answer 