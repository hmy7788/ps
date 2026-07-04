def solution(genres, plays):
    d = {g: [{}, 0, 0] for g in set(genres)}
    g = []
    answer = []
    
    for i, (k, v) in enumerate(zip(genres, plays)):
        d[k][0][i] = v
        d[k][1] += v
        d[k][2] += 1
        
    for v in d.values():
        g.append(v)
    
    g.sort(key=lambda x: x[1], reverse=True)
    
    for i in g:
        sorted_songs = sorted(i[0].items(), key=lambda x: (-x[1], x[0]))
        
        for song_id, play_cnt in sorted_songs[:2]:
            answer.append(song_id)
    
    return answer