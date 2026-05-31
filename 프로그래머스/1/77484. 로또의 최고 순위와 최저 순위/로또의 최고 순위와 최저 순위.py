def solution(lottos, win_nums):
    score_board = {6:1, 5:2, 4:3, 3:4, 2:5, 1:6, 0:6}
    match_count = 0
    zero_count = 0
    
    for i in lottos:
        if(i in win_nums):
            match_count += 1
        if(i == 0):
            zero_count += 1
    max_score = match_count + zero_count
    min_score = match_count
    answer = [score_board[max_score], score_board[min_score]]
    
    return answer