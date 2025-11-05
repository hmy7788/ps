T = int(input())
for _ in range(T):
    C = int(input())
    # 쿼터 = 0.25
    quarter_cnt = C // 25
    C %= 25

    # 다임 = 0.1
    dime_cnt = C // 10
    C %= 10

    # 니켈 = 0.05
    nickel_cnt = C // 5
    C %= 5

    # 페니 = 0.01
    penny_cnt = C // 1
    C %= 1
    print(f'{quarter_cnt} {dime_cnt} {nickel_cnt} {penny_cnt}')