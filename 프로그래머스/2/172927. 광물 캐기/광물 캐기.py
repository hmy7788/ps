def solution(picks, minerals):
    minerals = minerals[:sum(picks)*5]
    bundles = []
    i, tired = 0, 0
    
    while i < len(minerals):
        bundles.append(minerals[i:i+5])
        i += 5
        
    groups = []
    for _ in range(len(bundles)):
        groups.append([0, 0, 0])
    
    for i, b in enumerate(bundles):
        for m in b:
            if m == 'diamond': groups[i][0] += 1
            elif m == 'iron': groups[i][1] += 1
            else: groups[i][2] += 1
            
    groups.sort(key=lambda x : (x[0], x[1], x[2]), reverse=True)
    
    for dia, iron, stone in groups:
        if picks[0] > 0:
            picks[0] -= 1
            tired += dia + iron + stone
            continue
        elif picks[1] > 0:
            picks[1] -= 1
            tired += dia * 5 + iron + stone
            continue
        elif picks[2] > 0:
            picks[2] -= 1
            tired += dia * 25 + iron * 5 + stone
            continue
        
    return tired