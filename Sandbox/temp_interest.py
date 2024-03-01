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
    ir_factor = perc/12
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

def home_appreciation(mortgage: float, time: int, rate: float = 0.05) -> float:
    """
    
    
        Factors:
        - Initial Home Value
        - Equity
        - Interest Paid
        - Appreciation accrued
    """
    return mortgage*math.pow(1+rate, time)

if __name__ == "__main__":
    # I need more skills for this, make more progress on agri-scripts first before I return to this issue
    timespan = 120 # months

    savings = 2000
    invest = 1000
    mortgage = 3000

    # savings_total = repeating_investment(savings, 0.043, timespan/12, 1)
    # print(f"Saved = {savings_total}")
    # invest_total = repeating_investment(invest, 0.06, timespan/12, 1)
    # print(f"Invested = {invest_total}")

    # education = 10000
    # home_init = 350000
    # home_app = home_appreciation(home_init, timespan/12, 0.05)
    # print(f"Home Value = {home_app}")

    # gross = savings_total + invest_total + home_app
    # print(f"\nGross Worth after {timespan} months: {gross}")

    # debt = education + home_init
    # print(f"Debt after {timespan} months: {debt}")

    # net = gross - debt
    # print(f"Net Worth after {timespan} months: {net}")

    # # bill = float(input("Enter the recurring amount: "))
    # # months = float(input("How many months between payments? (3 would be quarterly): "))
    # # interest = float(input("What interest will apply? (can be 0): "))
    sav_interest = 0.0433
    inv_interest = 0.07

    print()
    print(f"You would save ${repeating_investment(savings, sav_interest, 1, 1)} over 1 year ({int(sav_interest*100)}% interest)")
    print(f"You would save ${repeating_investment(savings, sav_interest, 2, 1)} over 2 years ({int(sav_interest*100)}% interest)")
    print(f"You would save ${repeating_investment(savings, sav_interest, 3, 1)} over 3 years ({int(sav_interest*100)}% interest)")
    print()
    print(f"You would invest ${repeating_investment(invest, inv_interest, 1, 1)} over 1 year ({int(inv_interest*100)}% interest)")
    print(f"You would invest ${repeating_investment(invest, inv_interest, 2, 1)} over 2 years ({int(inv_interest*100)}% interest)")
    print(f"You would invest ${repeating_investment(invest, inv_interest, 3, 1)} over 3 years ({int(inv_interest*100)}% interest)")
    print()
    print(f"After student loans are paid off, you will have an additional ${repeating_investment(2250, sav_interest, 1, 1)} on year 2")
    print(f"After student loans are paid off, you will have an additional ${repeating_investment(2250, sav_interest, 2, 1)} on year 3")
    # print(f"You would save ${repeating_investment(bill, interest, 10, months)} over 10 years ({int(interest*100)}% interest)")
