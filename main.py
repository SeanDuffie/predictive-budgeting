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
    TL3 = datetime.date(2034, 1, 1)
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
    from bokeh.io import curdoc
    from bokeh.models import ColumnDataSource, DatetimeTickFormatter, Select, NumeralTickFormatter
    from math import radians
    import numpy as np

    import pandas as pd

    RTDIR = os.path.dirname(__file__)

    # create a pandas dataframe
    df1 = portfolio.loans["Student Loan #1"].plan
    df1["Date"] = pd.to_datetime(df1["Date"])

    df2 = portfolio.savings["American Express HYSA"].history
    df2["Date"] = pd.to_datetime(df2["Date"])

    curdoc().theme = 'night_sky'

    # create a Bokeh figure
    # p = bokeh.plotting.figure(title="Loan Change", x_axis_label='Date', y_axis_label='Amount')
    p = bokeh.plotting.figure(
        title="Loan Change",
        x_axis_label='Date (years)',
        x_axis_type='datetime',
        y_axis_label='Amount',
        y_axis_type='linear',
        width=1200,
        height=600
    )

    # add a line renderer to the figure
    p.line(x=df1['Date'], y=df1['Balance Remaining'], line_width=2, line_color='blue')
    p.line(x=df1['Date'], y=df1['Total Interest'], line_width=2, line_color='red')

    # add a line renderer to the figure
    p.line(x=df2['Date'], y=df2['Balance'], line_width=2, line_color='green')
    
    
    # Format graph
    date_pattern = ["%Y-%m-%d"]
    p.xaxis.formatter = DatetimeTickFormatter(
        days = date_pattern,
        months = date_pattern,
        years = date_pattern
    )
    p.xaxis.major_label_orientation=radians(80)
    p.yaxis.formatter = NumeralTickFormatter(format="$0,0.00")

    # bokeh.plotting.output_file()
    bokeh.plotting.save(p, filename=f"{RTDIR}/NetWorth.html", title="Net Worth Projection")

    html = bokeh.embed.file_html(p)
    # print(f"{html=}\n\n\n")

    # json = bokeh.embed.json_item(p)
    # print(f"{json=}")

    # show the figure
    bokeh.plotting.show(p)
