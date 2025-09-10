def can_place(i, j, mat, park):
    H, W = len(park), len(park[0])
    
    if(i+mat > H or j+mat > W):
        return False
    else:
        for p in range(i, i+mat):
            for q in range(j, j+mat):
                if(park[p][q] != '-1'):
                    return False
        return True
                
def solution(mats, park):
    H, W = len(park), len(park[0])
    mats.sort(reverse=True)
    
    for mat in mats:
        for i in range(H):
            for j in range(W):
                if(can_place(i, j, mat, park)):
                    return mat
    return -1
                
            
            
