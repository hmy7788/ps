def solution(n, words):
    word_hm = [words[0]]
    people_hm = {i: 0 for i in range(1, n+1)}
    people_hm[1] = 1
    k = 2
    
    for i in range(1, len(words)):
        if k > n:
            k = 1
        current_word = words[i]
        prev_word = words[i-1]
        
        if prev_word[-1] == current_word[0] and current_word not in word_hm:
            people_hm[k] += 1
            word_hm.append(current_word)
            k += 1
        else:
            return [k, people_hm[k]+1]
    
    return [0, 0]