def solution(routes):
    routes.sort(key=lambda x:x[1])
    camera_point = float('-inf')
    camera_cnt = 0
    
    for sp, ep in routes:
        if camera_point == float('-inf'):
            camera_point = ep
            camera_cnt += 1
            continue
        if sp <= camera_point <= ep:
            continue
        elif camera_point < sp:
            camera_point = ep
            camera_cnt += 1
    
    return camera_cnt