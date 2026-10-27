import heapq

def solution(book_time):
    rooms = []
    heapq.heapify(rooms)
    room_cnt = 0
    
    for i, bt in enumerate(book_time):
        start, end = bt[0], bt[1]
        sh, sm = start.split(':')
        eh, em = end.split(':')
        start, end = 60 * int(sh) + int(sm), 60 * int(eh) + int(em) + 10
        book_time[i][0], book_time[i][1] = start, end

    book_time.sort(key=lambda x:x[0])
    
    for start, end in book_time:
        if rooms:
            if start < rooms[0]:
                heapq.heappush(rooms, end)
                room_cnt += 1
            else:
                heapq.heappop(rooms)
                heapq.heappush(rooms, end)
        else:
            heapq.heappush(rooms, end)
            room_cnt += 1
            
    return room_cnt