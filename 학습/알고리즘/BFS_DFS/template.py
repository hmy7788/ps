from collections import deque, defaultdict

def bfs(graph, v, N):
    dq = deque()
    visited = [0] * (N+1)
    visited[v] = 1
    dq.append(v)
    answer = [v]
    
    while dq:
        node = dq.popleft()

        for n in graph[node]:
            if visited[n] == 0:
                visited[n] = 1
                answer.append(n)
                dq.append(n)
        
    return answer


def dfs_recursive(graph, v, visited, answer):
    if visited[v] != 0:
        return answer
    
    visited[v] = 1
    answer.append(v)

    for n in graph[v]:
        dfs_recursive(graph, n, visited, answer)
    
    return answer


def dfs_iterative(graph, v, N):
    stack = deque()
    visited = [0] * (N+1)
    visited[v] = 1
    stack.append(v)
    answer = [v]

    while stack:
        node = stack.pop()

        for n in reversed(graph[node]):
            if visited[n] == 0:
                visited[n] = 1
                answer.append(n)
                stack.append(n)

    return answer

if __name__ == '__main__':
    input_data = (
        [[4, 5, 1],
        [1, 2],
        [1, 3],
        [1, 4],
        [2, 4],
        [3, 4]],
        [[5, 5, 3],
        [5, 4],
        [5, 2],
        [1, 2],
        [3, 4],
        [3, 1]],
        [[1000, 1, 1000],
        [999, 1000]]
    )

    for case in input_data:
        N, M, V = case[0]
        edges = case[1:]

        graph = defaultdict(list)
        for i, j in edges:
            graph[i].append(j)
            graph[j].append(i)

        for k in graph.keys():
            graph[k].sort()

        visited = [0] * (N+1)
        answer = []

        
        print(f"{' '.join(map(str, dfs_iterative(graph, V, N)))}")
        print(f"{' '.join(map(str, dfs_recursive(graph, V, visited, answer)))}")
        print(f"{' '.join(map(str, bfs(graph, V, N)))}\n")