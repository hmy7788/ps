def checking_angle():
    pass

def solution(wallet, bill):
    count = 0
    while(min(bill) > min(wallet) or max(bill) > max(wallet)):
        if(bill[0] > bill[1]):
            bill[0] = int(bill[0] / 2)
        else:
            bill[1] = int(bill[1] / 2)
        count += 1
    return count