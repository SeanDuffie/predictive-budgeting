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
    portfolio = Portfolio("net_worth.db", start=datetime.date(2024, 1, 1))

    # Student Loans 1
    portfolio.add_loan(
        start=datetime.date(2024, 3, 5),
        end=datetime.date(2033, 9, 5),
        amount=5677.25,
        apr=.025,
        name="Student Loan #1"
    )

    # Student Loans 2
    portfolio.add_loan(
        start=datetime.date(2024, 3, 5),
        end=datetime.date(2033, 9, 5),
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
        # apr=0.0435,
        apr=0.1,
        recur=new_budget["HYSA (Emergency)"],
        name="American Express HYSA"
    )

    # Stock Portfolio
    portfolio.add_investment(
        deposit=10000,
        start=datetime.date(2024, 3, 5),
        apr=0.1,
        recur=new_budget["Investments"],
        name="Stocks"
    )

    # Home cost is an Asset
    HOME_VAL = 330000
    PURCHASE_DATE = datetime.date(2025, 3, 1)
    portfolio.update_all(PURCHASE_DATE)
    portfolio.add_asset(
        init_value=HOME_VAL,
        start=PURCHASE_DATE,
        apr=0.08,
        name="House"
    )

    # Down payment is subtracted from savings
    DOWN_PAYMENT = HOME_VAL * 0.1
    portfolio.savings["American Express HYSA"].modify_balance(-DOWN_PAYMENT, PURCHASE_DATE, "Placed down payment on house")

    # Mortgage is home cost minus down payment
    MORT = HOME_VAL - DOWN_PAYMENT
    # MORT_DATE = PURCHASE_DATE + datetime.timedelta(3650)
    MORT_DATE = PURCHASE_DATE + datetime.timedelta(5475)
    MORT_TERM = 120
    portfolio.add_loan(
        start=PURCHASE_DATE,
        end=MORT_DATE,
        amount=MORT,
        apr=.06,
        name="Mortgage"
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
    # df1 = portfolio.loans["Student Loan #1"].plan
    # df1["Date"] = pd.to_datetime(df1["Date"])

    # df2 = portfolio.savings["American Express HYSA"].history
    # df2["Date"] = pd.to_datetime(df2["Date"])

    retirement = datetime.date(2067, 5, 1)
    df = portfolio.project_net(retirement)

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

    # Add a line renderer to the figure
    p.line(x=df['Date'], y=df['Net'], legend_label="Net", line_width=8, line_color='green')
    p.line(x=df['Date'], y=df['Gross'], legend_label="Gross", line_width=1, line_dash=(4, 4), line_color='lime')
    p.line(x=df['Date'], y=-df['Debt'], legend_label="Debt", line_width=1, line_dash=(4, 4), line_color='red')
    p.line(x=df['Date'], y=df['Savings'], legend_label="Savings", line_width=1, line_color='yellow')
    p.line(x=df['Date'], y=df['Investments'], legend_label="Investments", line_width=1, line_color='purple')
    p.line(x=df['Date'], y=df['Assets'], legend_label="Assets", line_width=1, line_color='pink')

    p.legend.title = "Categories"
    p.title.text = "Net Worth"
    p.title.align = "center"
    p.legend.location = "top_left"

    # Format graph
    # date_pattern = "%Y/%m"
    p.xaxis.formatter = DatetimeTickFormatter(
        days = "%Y / %m / %d",
        months = "%Y / %m",
        years = "%Y"
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
