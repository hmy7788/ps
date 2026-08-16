import heapq

def solution(dataSize, processingTime):
    servers = []
    n = len(dataSize)

    def check_using_server(t):
        if len(servers) == 0:
            return False, None

        else:
            finish_t = servers[0][0]
            if t < finish_t:
                return False, None
            else:
                return True, finish_t
    
    for t in range(n):
        flag, finish_t = check_using_server(t)

        if flag:
            top = heapq.heappop(servers)
            top[0] += (t-finish_t) + processingTime[t]
            top[1] += dataSize[t]
            heapq.heappush(servers, top)

        else:
            heapq.heappush(servers, [t+processingTime[t], dataSize[t]])

        # print(f't={t}, {servers}')

    max_data_sum = float('-inf')
    for s in servers:
        data_sum = s[1]
        if max_data_sum < data_sum:
            max_data_sum = data_sum

    return max_data_sum


if __name__ == '__main__':
    ds1 = [4, 4, 2, 2, 3, 1, 5, 2]
    pt1 = [4, 2, 4, 1, 2, 1, 1, 1]

    ds2 = [3, 1, 4]
    pt2 = [1, 1, 1]

    ds3 = [2, 7, 4]
    pt3 = [5, 5, 5]

    print(solution(ds3, pt3))

    '''
    '''