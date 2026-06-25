import random

def bubble_sort(arr):
    n = len(arr)

    for i in range(n):
        for j in range(1, n-i):
            if arr[j-1] > arr[j]:
                arr[j-1], arr[j] = arr[j], arr[j-1]
    
    return arr

def select_sort(arr):
    for i in range(len(arr)-1):
        min_idx = i
        for j in range(i+1, len(arr)):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[min_idx], arr[i] = arr[i], arr[min_idx]
    
    return arr

if __name__ == '__main__':
    arr = random.sample(range(1, 51), 10)
    
    print(bubble_sort(arr.copy()))
    print(select_sort(arr.copy()))

    arr = [
    [25, 'Minyeop_A'],
    [21, 'Chaeun'], 
    [25, 'Minyeop_B'], 
    [23, 'Byeongju'], 
    [25, 'Minyeop_C']
]
    arr.sort(key=lambda x : x[0])
    print(arr)