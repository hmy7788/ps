def solution(brown, yellow):
    result = []
    
    for i in range(1, yellow+1):
        if yellow % i == 0:
            row = i
            col = int(yellow / i)
            
            if (row + col + 2) * 2 == brown:
                if row <= col:
                    result.append(col)
                    result.append(row)
                else:
                    result.append(row)
                    result.append(col)
                break
                
    return [result[0]+2, result[1]+2]