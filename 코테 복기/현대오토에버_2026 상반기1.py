def solution1(w, h, dst_nodes): # 완전 탐색으로 푼 문제
    perms = []
    n = len(dst_nodes)
    v = [0] * n

    def dfs(current_perm):
        if len(current_perm) == n:
            perms.append(current_perm[:])
            return 
        
        for i in range(n):
            node = dst_nodes[i]
            if v[i] == 0:
                current_perm.append(node)
                v[i] = 1
                dfs(current_perm)
                current_perm.pop()
                v[i] = 0
    
    dfs([])

    def calc_distance(i, j):
        iy, ix = (i-1)//w, (i-1)%w
        jy, jx = (j-1)//w, (j-1)%w

        return abs(iy-jy) + abs(ix-jx)

    min_dist = float('inf')

    for p in perms:
        route = [1] + p
        dist = 0
        for i in range(1, len(route)):
            dist += calc_distance(route[i-1], route[i])
        
        if min_dist > dist:
            min_dist = dist

    return min_dist


def solution2(w, h, dst_nodes):
    nodes = [1] + dst_nodes
    n = len(nodes)

    dp = [[-1 for _ in range(2**n)] for _ in range(n)]

    def calc_distance(i, j):
        iy, ix = (i-1)//w, (i-1)%w
        jy, jx = (j-1)//w, (j-1)%w
        return abs(iy-jy)+abs(ix-jx)
    
    def dfs(curr, visited):
        if visited == 2**n-1:
            return 0
        
        if dp[curr][visited] != -1:
            return dp[curr][visited]

        min_dist = float('inf')

        for next_node in range(n):
            if visited & (1 << next_node) == 0:
               new_visited = visited | (1 << next_node)
               dist = calc_distance(nodes[curr], nodes[next_node]) + dfs(next_node, new_visited) 
               min_dist = min(min_dist, dist)

        dp[curr][visited] = min_dist

        return dp[curr][visited]

    return dfs(0, 1)

if __name__ == '__main__':
    print('완전 탐색으로 푼 문제: O(N!)')
    print(solution1(5, 2, [5, 8, 10]))
    print(solution1(5, 5, [3, 23]))
    print(solution1(5, 5, [4, 7, 9, 14, 17, 20, 25]))

    print('\n비트마스킹 + dp로 푼 문제: O(N^2 * 2^N)')
    print(solution2(5, 2, [5, 8, 10]))
    print(solution2(5, 5, [3, 23]))
    print(solution2(5, 5, [4, 7, 9, 14, 17, 20, 25]))