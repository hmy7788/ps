from itertools import permutations

def node_to_xy(w, h, node):
    st = 1
    for i in range(h):
        for j in range(w):
            if st == node:
                return i, j
            st += 1

def distance(n1, n2):
    n1_x, n1_y = n1[0], n1[1]
    n2_x, n2_y = n2[0], n2[1]

    return abs(n1_x-n2_x) + abs(n1_y-n2_y)

def solution(w, h, dst_nodes):
    
    min_dist = float('inf')
    root = None
    for perm in permutations(dst_nodes):
        perm = list(perm)
        perm.insert(0, 1)
        dist = 0
        for i in range(len(dst_nodes)):
            dist += distance(n1= node_to_xy(w, h, perm[i]), n2=node_to_xy(w, h, perm[i+1]))
            
        if dist < min_dist:
            min_dist = dist
            root = perm
    
    print(f'최소 거리: {min_dist}')
    print(f"최소 경로: {' -> '.join(map(str, root))}")
    print()

if __name__ == '__main__':
    solution(5, 2, [5, 8])
    solution(5, 5, [3, 23])
    solution(5, 5, [4, 7, 9, 14, 17, 20, 25])