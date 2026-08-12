def servers_check(servers, t):
    able_server_cnt = 0
    for start_time, end_time in servers:
        if start_time <= t < end_time:
            able_server_cnt += 1
            
    return able_server_cnt

def solution(players, m, k):
    cnt = 0
    servers = []
    
    for t, p in enumerate(players):
        if p < m: continue
        else:
            needs_server_cnt = p // m
            able_server_cnt = servers_check(servers, t)
            if needs_server_cnt > able_server_cnt:
                add_server_cnt = needs_server_cnt - able_server_cnt
                for _ in range(add_server_cnt):
                    servers.append([t, t+k])
                    cnt += 1
                    
    print(servers)
    
    return cnt