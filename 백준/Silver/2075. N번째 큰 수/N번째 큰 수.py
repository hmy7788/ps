import heapq

def solution(N, arr):
    heap = []
    row_ptr = [N-1] * N

    for i, a in enumerate(arr[-1]):
        heap.append((-a, a, i))
    heapq.heapify(heap)

    for _ in range(N-1):
        _, _, j = heapq.heappop(heap)
        row_ptr[j] -= 1
        i = row_ptr[j]
        heapq.heappush(heap, (-arr[i][j], arr[i][j], j))
    
    print(heap[0][1])
    

N = int(input())
arr = []
for _ in range(N):
    arr.append(list(map(int, input().split())))

solution(N, arr)