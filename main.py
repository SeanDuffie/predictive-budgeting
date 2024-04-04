""" @file main.py
    @author Sean Duffie
    @brief This is the main runner for the predictive budgeting application
"""
import datetime

from budget.budget import Budget
from portfolio import Portfolio

if __name__ == "__main__":
    # Launch portfolio (this shouldn't need branches, since each will be paired with a budget)
    # Generate graphs for projections into the future
    portfolio = Portfolio("net_worth.db")

    # Student Loans 1
    portfolio.add_loan(
        start=datetime.datetime(2024, 3, 5),
        end=datetime.datetime(2033, 9, 5),
        amount=5677.25,
        apr=.025,
        name="Student Loan #1"
    )

    # Student Loans 2
    portfolio.add_loan(
        start=datetime.datetime(2024, 3, 5),
        end=datetime.datetime(2033, 9, 5),
        amount=4777.83,
        apr=.0348,
        name="Student Loan #2"
    )

    # Set up budget (branches?)
    # Set up income (branches? to compare multiple incomes)
    # Calculate taxes and net income
    budget = Budget(gross=104000, state="GA")
    # Get min debt payments from Loans
    for loan in portfolio.loans.values():
        budget.add_minimum_payments(loan.payment)
    # Get living expenses
    new_budget = budget.generate_budget()
    # Mark growth payments (Extra Loan, Savings, Investments)
    # Calculate remaining spending money
    budget.apply_budget(new_budget)
    budget.gen_percents(new_budget)

    # American Express HYSA
    portfolio.add_savings(
        deposit=10000,
        start=datetime.date(2024, 3, 5),
        apr=0.0435,
        recur=new_budget["HYSA (Emergency)"],
        name="American Express HYSA"
    )

    # Stock Portfolio
    portfolio.add_savings(
        deposit=10000,
        start=datetime.date(2024, 3, 5),
        apr=0.07,
        recur=new_budget["Investments"],
        name="Stocks"
    )

    # Project into the future
    TL3 = datetime.date(2026, 1, 1)
    portfolio.update_all(TL3)
    portfolio.calculate_net(TL3)
    portfolio.calculate_ratio(TL3)

    # print("\nHYSA history:")
    # for event in portfolio.savings["American Express HYSA"].history.iterrows():
    #     print(f"\t{event}")

    # print("\nETRADE history:")
    # for event in portfolio.savings["Stocks"].history.iterrows():
    #     print(f"\t{event}")

    # Ask if user wants to save to a database
    import os

    import bokeh.embed
    import bokeh.plotting
    import pandas as pd

    RTDIR = os.path.dirname(__file__)

    # create a pandas dataframe
    # df = pd.DataFrame({'date': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03']), 'value': [1, 2, 3]})
    df = portfolio.loans["Student Loan #1"].plan
    df["Date"] = pd.to_datetime(df["Date"])

    # create a Bokeh figure
    p = bokeh.plotting.figure(title="Loan Change", x_axis_label='Date', y_axis_label='Amount')

    # add a line renderer to the figure
    p.line(x=df['Date'], y=df['Balance Remaining'], line_width=2)
    p.line(x=df['Date'], y=df['Applied to Principal'], line_width=2)
    p.line(x=df['Date'], y=df['Applied to Interest'], line_width=2)
    p.line(x=df['Date'], y=df['Total Interest'], line_width=2)

    # bokeh.plotting.output_file()
    bokeh.plotting.save(p, filename=f"{RTDIR}/Loans.html")

    html = bokeh.embed.file_html(p)
    # print(f"{html=}\n\n\n")

    # json = bokeh.embed.json_item(p)
    # print(f"{json=}")

    # show the figure
    # bokeh.plotting.show(p)

    df = portfolio.savings["American Express HYSA"].history
    df["Date"] = pd.to_datetime(df["Date"])

    # create a Bokeh figure
    p = bokeh.plotting.figure(title="Savings Change", x_axis_label='Date', y_axis_label='Amount')

    # add a line renderer to the figure
    p.line(x=df['Date'], y=df['Balance'], line_width=2)
    p.line(x=df['Date'], y=df['Change'], line_width=2)

    # bokeh.plotting.output_file()
    bokeh.plotting.save(p, filename=f"{RTDIR}/Savings.html")

    html = bokeh.embed.file_html(p)
    # print(f"{html=}\n\n\n")

    # json = bokeh.embed.json_item(p)
    # print(f"{json=}")

    # show the figure
    # bokeh.plotting.show(p)

