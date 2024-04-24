""" @file app.py
    @author Sean Duffie
    @brief Flask Framework to host the web user interface with the budgeting program

    This website allows a more convenient way for the user to utilize the budgeting tools.
    Additionally, this will display the Bokeh data visualization tools and potentially allow users
    to store and load data.

    Resources:
    - https://www.digitalocean.com/community/tutorials/how-to-use-web-forms-in-a-flask-application
"""
import datetime
import logging
import os
from math import radians

import bokeh.embed
import bokeh.layouts
import bokeh.models
import bokeh.plotting
import pandas as pd
from flask import Flask, flash, redirect, render_template, request, url_for

import logFormat
from portfolio import Portfolio

# Initial Logger Settings
logFormat.format_logs(logger_name=__name__)
logger = logging.getLogger(__name__)

WIDTH = 1200
HEIGHT = 600


RTDIR = os.path.dirname(__file__)
app = Flask(
    import_name=__name__,
    static_folder=f"{RTDIR}/web/static",
    template_folder=f"{RTDIR}/web/templates"
)
app.config['SECRET_KEY'] = '1d2e3382586f37723ba8aad13ece71d521e2b6fd1d0e7407'

AGE = 23
START = datetime.date(2024, 2, 1)
END = datetime.date(2067, 6, 1)

# portfolio = Portfolio("net_worth.db")
pfs = [Portfolio(
            "net_worth.db",
            start=START,
            end=END,
            age=AGE
        )]
messages: dict = []

@app.route("/", methods = ["GET", "POST"])
def index():
    plot = bokeh.plotting.figure(
        title="Loan Change",
        x_axis_label='Date (years)',
        x_axis_type='datetime',
        y_axis_label='Amount',
        y_axis_type='linear',
        width=WIDTH,
        height=HEIGHT,
        align="center"
    )

    if request.method == "POST":
        age = request.form.get("age")
        start = datetime.date.fromisoformat(request.form.get("income1start"))
        end = datetime.date.fromisoformat(request.form.get("income1end"))

        pfs.append(
            Portfolio(
                "net_worth.db",
                start=start,
                end=end,
                age=age
            )
        )

    for scenario in pfs:
        df = scenario.project_net(date=END)
        plot.line(x=df['Date'], y=df['Net'], legend_label="Net", line_width=4, line_color='green')
        plot.line(x=df['Date'], y=df['Gross'], legend_label="Gross", line_width=2, line_color='blue')
        plot.line(x=df['Date'], y=df['Debt'], legend_label="Debt", line_width=2, line_color='red')

    plot.legend.title = "Categories"
    plot.legend.location = "top_left"

    # Format graph
    plot.xaxis.formatter = bokeh.models.DatetimeTickFormatter(
        days = "%Y / %m / %d",
        months = "%Y / %m",
        years = "%Y"
    )
    plot.xaxis.major_label_orientation=radians(80)
    plot.yaxis.formatter = bokeh.models.NumeralTickFormatter(format="$0,0.00")

    # Add the select bar
    source = bokeh.models.ColumnDataSource( data=df )
    select = bokeh.plotting.figure(title="Drag the middle and edges of the selection box to change the range above",
                    height=100, width=WIDTH, y_range=plot.y_range,
                    x_axis_type="datetime", y_axis_type=None,
                    tools="", toolbar_location=None, background_fill_color="#efefef")

    range_tool = bokeh.models.RangeTool(x_range=plot.x_range)
    range_tool.overlay.fill_color = "navy"
    range_tool.overlay.fill_alpha = 0.2

    select.line('Date', 'Net', source=source)
    select.ygrid.grid_line_color = None
    select.add_tools(range_tool)

    # plot.y_range.start = df["Net"].min() - ((df["Net"].max()-df["Net"].min()+1) * 0.05)
    # plot.y_range.end = df["Net"].max() + ((df["Net"].max()-df["Net"].min()+1) * 0.05)

    # Attach the Select Tool to the main figure
    col = bokeh.layouts.column(plot, select)

    # bokeh.plotting.show(col)
    script, div = bokeh.embed.components(col)

    # NOTE: Jinja has a feature called auto-escaping, which automatically escapes any values sent
    # to it, like using "\n" or "\\" in python strings. This can be disabled by either adding the
    # "|safe" suffix to the end of the Jinja call, or by calling markupsafe.Markup() on the block.
    # This can also be done by adding an "{% autoescape false %} - {% endautoescape %}" block.
    return render_template(
        "index.html",
        portfolios=pfs,
        script=script,
        div=div
    )

@app.route('/form_savings/', methods=('GET', 'POST'))
def form_savings():
    if request.method == 'POST':
        name = request.form.get("name")
        start = datetime.date.fromisoformat(request.form.get("start"))
        amount = float(request.form.get("amount"))
        recur = float(request.form.get("recur"))
        apr = float(request.form.get("apr"))

        # Handle errors and send back to index if successful
        # if num is None:
        #     flash('Must select a Portfolio')
        # elif num < 0 or num >= len(pfs):
        #     flash('Choose a valid portfolio')
        if not start:
            flash('Start date is required!')
        elif not amount:
            flash('Starting balance is required!')
        elif not apr:
            flash('APR is required!')
        elif not name:
            flash('Asset Name is required!')
        else:
            messages.append({'Name': name, 'Amount': amount, "Recurring": recur, 'APR': apr, 'start': start})
            pfs[0].add_savings(deposit=amount, start=start, recur=recur, apr=apr, name=name)
            return redirect(url_for('index'))

    return render_template('form_savings.html')

@app.route('/form_investment/', methods=('GET', 'POST'))
def form_investment():
    if request.method == 'POST':
        # num = int(request.form["portfolio"])
        name = request.form.get("name")
        start = datetime.date.fromisoformat(request.form.get("start"))
        amount = float(request.form.get("amount"))
        recur = float(request.form.get("recur"))
        apr = float(request.form.get("apr"))

        # Handle errors and send back to index if successful
        # if num is None:
        #     flash('Must select a Portfolio')
        # elif num < 0 or num >= len(pfs):
        #     flash('Choose a valid portfolio')
        if not start:
            flash('Start date is required!')
        elif not amount:
            flash('Starting balance is required!')
        elif not apr:
            flash('APR is required!')
        elif not name:
            flash('Asset Name is required!')
        else:
            messages.append({'Name': name, 'Amount': amount, "Recurring": recur, 'APR': apr, 'start': start})
            pfs[0].add_investment(deposit=amount, start=start, recur=recur, apr=apr, name=name)
            return redirect(url_for('index'))

    return render_template('form_investment.html')

    # <a href="{{ url_for('form_budget') }}">Add Budget</a>
    # <a href="{{ url_for('form_loan') }}">Add Loan</a>
    
@app.route('/form_asset/', methods=('GET', 'POST'))
def form_asset():
    if request.method == 'POST':
        # num = int(request.form["portfolio"])
        name = request.form.get("name")
        start = datetime.date.fromisoformat(request.form.get("start"))
        amount = float(request.form.get("amount"))
        apr = float(request.form.get("apr"))

        # Handle errors and send back to index if successful
        # if num is None:
        #     flash('Must select a Portfolio')
        # elif num < 0 or num >= len(pfs):
        #     flash('Choose a valid portfolio')
        if not start:
            flash('Start date is required!')
        elif not amount:
            flash('Starting balance is required!')
        elif not apr:
            flash('APR is required!')
        elif not name:
            flash('Asset Name is required!')
        else:
            messages.append({'Name': name, 'Amount': amount, 'APR': apr, 'start': start})
            pfs[0].add_asset(init_value=amount, start=start, apr=apr, name=name)
            return redirect(url_for('index'))

    return render_template('form_asset.html')

@app.route('/form_loan/', methods=('GET', 'POST'))
def form_loan():
    if request.method == 'POST':
        # num = int(request.form["portfolio"])
        name = request.form.get("name")
        start = datetime.date.fromisoformat(request.form.get("start"))
        amount = float(request.form.get("amount"))
        apr = float(request.form.get("apr"))
        term = int(request.form.get("term"))

        # Handle errors and send back to index if successful
        # if num is None:
        #     flash('Must select a Portfolio')
        # elif num < 0 or num >= len(pfs):
        #     flash('Choose a valid portfolio')
        if not start:
            flash('Start date is required!')
        elif not amount:
            flash('Starting balance is required!')
        elif not apr:
            flash('APR is required!')
        elif not name:
            flash('Asset Name is required!')
        elif not term:
            flash('Term length required!')
        else:
            messages.append({'Name': name, 'Amount': amount, 'APR': apr, 'start': start, 'term': term})
            pfs[0].add_loan(amount=amount, start=start, term=term, apr=apr, name=name)
            return redirect(url_for('index'))

    return render_template('form_asset.html')

@app.route('/budget/', methods=['GET', 'POST'])
def budget():
    return render_template('budget.html')

@app.route('/house_cost/', methods=['GET', 'POST'])
def house_cost():
    return render_template('house_cost.html')

if __name__ == "__main__":
    print(RTDIR)
    app.run(debug=True)
