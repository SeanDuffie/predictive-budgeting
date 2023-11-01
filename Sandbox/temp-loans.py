""" temp_loans.py

Calculate the total interest generated and repayment time of a student loan based on the amount
contributed from a paycheck every two weeks.

Interest on student loans is compounded daily, and I'm contributing a certain amount each paycheck
(twice a month) towards paying off these loans.

Reference:
https://lendedu.com/blog/how-does-student-loan-interest-work/
"""

initial = 15000
fixed_rate = 0.0375
ir_factor = fixed_rate/365

payment = int(input("How much per paycheck? "))
remaining = initial
total_interest = 0

c = 0
while remaining > payment:
    for _ in range(14):
        current_interest = remaining * ir_factor
        total_interest += current_interest
        remaining += current_interest
    remaining -= payment
    c+=1
    print(f"Payment {c} | Total interest={total_interest} | Remaining={remaining}")
print(f"Final Payment {c} | Total interest={total_interest} | Last Bill={remaining} | Duration={c/26} years")