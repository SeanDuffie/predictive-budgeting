""" temp_interest.py

This program was made to help simulate how much you would save by cancelling a monthly expense.
It assumes that you would be generating interest on money not spent, and can be used to esimate
either total amount put into savings, or just what you would be saving by not paying for one
subscription.

Amounts:
30 - 1-2 years of salary
40 - 3-4 years of salary
50 - 7 years of salary
"""

import math

bill = float(input("Enter the recurring amount: "))
months = float(input("How many months between payments? (3 would be quarterly): "))
interest = float(input("What interest will apply? (can be 0): "))

# one = math.pow(bill*(1+interest), 1)
# five = math.pow(bill*(1+interest), 5)
# ten = math.pow(bill*(1+interest), 10)

def repeating_investment(amnt: float, perc: float, time: int, interval: float = 1):
    """_summary_

    Args:
        amnt (float): the amount being contributed per cycle
        perc (float): the interest rate of investment (percentage), could be 0
        time (int): how many years are remaining in the calculation
        interval (float, optional): Time between charges in months, 3 is quarterly, 0.5 is bi-weekly. Defaults to 1.
            - FIXME: Interest calculations don't work for bi-weekly (paychecks) b/c monthly compounding

    Returns:
        float: amount with recent deposits and interest, used recursively
    """
    per_year = 12/interval
    ir_factor = interest/12
    new_amnt = 0

    if time > 1:
        new_amnt = repeating_investment(amnt, perc, time-1, interval)

    c = 0
    # print(f"{time} | {c}. {new_amnt} | {per_year}")
    while c < per_year:
        # Because the principal is being added to every interval, interest behaves differently
        new_amnt = (amnt + new_amnt) * (1 + ir_factor)
        c+=1
        # print(f"{time} | {c}. {new_amnt}")

    # print(f"Year {time}: ${new_amnt}")
    return new_amnt

# print(f"You would save ${one} over 1 year")
# print(f"You would save ${five} over 5 years")
# print(f"You would save ${ten} over 10 years")

print(f"You would save ${repeating_investment(bill, interest, 1, months)} over 1 year ({int(interest*100)}% interest)")
print(f"You would save ${repeating_investment(bill, interest, 5, months)} over 5 years ({int(interest*100)}% interest)")
print(f"You would save ${repeating_investment(bill, interest, 10, months)} over 10 years ({int(interest*100)}% interest)")
