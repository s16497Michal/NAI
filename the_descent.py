'''
autor = Michał Kosiński
problem = https://www.codingame.com/ide/puzzle/the-descent
'''

while True:
    # ustawiam początkowe limity
    max_mountain = 0
    max_mountain_index = 0

    for i in range(8):
        mountainH = int(input())

        # Ustawiam najwyzsza górę
        if mountainH > max_mountain:
            max_mountain = mountainH
            max_mountain_index = i

    print(max_mountain_index)