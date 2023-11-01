""" temp_interest.py

This program was made to help simulate how much you would save by cancelling a monthly expense.
It assumes that you would be generating interest on money not spent, and can be used to esimate
either total amount put into savings, or just what you would be saving by not paying for one
subscription.
"""

import math

bill = float(input("Enter the recurring amount: "))
interest = 0.07

# one = math.pow(bill*(1+interest), 1)
# five = math.pow(bill*(1+interest), 5)
# ten = math.pow(bill*(1+interest), 10)

def rec_int(amnt, perc, time):
    if time > 1:
        new_amnt = (bill+amnt)*(1+perc)
        new_time = time-1
        return rec_int(new_amnt, perc, new_time)
    return amnt*(1+perc)

# print(f"You would save ${one} over 1 year")
# print(f"You would save ${five} over 5 years")
# print(f"You would save ${ten} over 10 years")

print(f"You would save ${rec_int(bill, interest, 1)} over 1 year")
print(f"You would save ${rec_int(bill, interest, 5)} over 5 years")
print(f"You would save ${rec_int(bill, interest, 10)} over 10 years")
