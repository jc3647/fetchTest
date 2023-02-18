import pandas as pd
import sys

def main(total, file):

    # initialize things we need
    try:
        transactions = pd.read_csv(file).sort_values(by=['timestamp'])
    except:
        return 'invalid csv; usage: python fetch.py [points] [csv file]'
        
    total = int(total)
    payer_balances = {}

    for index, row in transactions.iterrows():
        # fill in hash table of payers
        user, points = row[0], row[1]
        if user not in payer_balances:
            payer_balances[user] = points
        else:
            payer_balances[user] += points

        if total == 0:
            continue
        # adjust total points accordingly
        if points > 0:
            payer_balances[user] -= min(total, points)
            total -= min(total, points)
        elif points < 0:
            payer_balances[user] += abs(points)
            total += abs(points)

    if total > 0:
        return "Too many points, payers don't have enough"
    
    return payer_balances


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('usage: python fetch.py [points] [csv file]')
    elif not sys.argv[1].isdigit():
        print('invalid points; usage: python fetch.py [points] [csv file]')
    else:
        print(main(sys.argv[1], sys.argv[2]))