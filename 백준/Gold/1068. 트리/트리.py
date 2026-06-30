def solution(N, nodes, R):
    tree = {i: [] for i in range(N)}
    cnt = 0
    root = 0

    for i, n in enumerate(nodes):
        if n == -1:
            root = i
        else:
            tree[n].append(i)

    def dfs(n):
        nonlocal cnt
        if len(tree[n]) == 0 and n == R:
            return

        if len(tree[n]) == 0:
            cnt += 1
            return
        
        if n == R:
            return

        for next_node in tree[n]:
            dfs(next_node)

    dfs(root)

    return cnt

if __name__ == '__main__':
    N = int(input())
    nodes = list(map(int, input().split()))
    R = int(input())

    print(solution(N, nodes, R))