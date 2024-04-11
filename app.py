""" @file app.py
    @author Sean Duffie
    @brief Flask Framework to host the web user interface with the budgeting program

    This website allows a more convenient way for the user to utilize the budgeting tools.
    Additionally, this will display the Bokeh data visualization tools and potentially allow users
    to store and load data.

    Resources:
    - https://www.digitalocean.com/community/tutorials/how-to-use-web-forms-in-a-flask-application
"""
import os
import datetime

import bokeh.embed
import bokeh.plotting
import bokeh.models
import pandas as pd
from flask import Flask, flash, redirect, render_template, request, url_for
from math import radians

from portfolio import Portfolio


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
        width=1200,
        height=600,
        align="center"
    )
    AGE = 23
    START = datetime.date(2024, 2, 1)
    END = datetime.date(2067, 6, 1)

    if request.method == "POST":
        AGE = request.form.get("age")
        START = datetime.date.fromisoformat(request.form.get("income1start"))
        END = datetime.date.fromisoformat(request.form.get("income1end"))

        pfs.append(
            Portfolio(
                "net_worth.db",
                start=START,
                end=END,
                age=AGE
            )
        )

    for scenario in pfs:
        df = scenario.project_net(date=END)
        plot.line(x=df['Date'], y=df['Net'], legend_label="Net", line_width=8, line_color='green')

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

    script, div = bokeh.embed.components(plot)

    # NOTE: Jinja has a feature called auto-escaping, which automatically escapes any values sent
    # to it, like using "\n" or "\\" in python strings. This can be disabled by either adding the
    # "|safe" suffix to the end of the Jinja call, or by calling markupsafe.Markup() on the block.
    # This can also be done by adding an "{% autoescape false %} - {% endautoescape %}" block.
    return render_template(
        "form.html",
        messages=messages,
        script=script,
        div=div
    )

@app.route('/add_asset/', methods=('GET', 'POST'))
def add_asset():
    if request.method == 'POST':
        num = int(request.form["portfolio"])
        name = request.form.get("name")
        start = datetime.date.fromisoformat(request.form.get("start"))
        amount = float(request.form.get("amount"))
        apr = float(request.form.get("apr"))

        # Handle errors and send back to index if successful
        if num is None:
            flash('Must select a Portfolio')
        elif num < 0 or num >= len(pfs):
            flash('Choose a valid portfolio')
        elif not start:
            flash('Start date is required!')
        elif not amount:
            flash('Starting balance is required!')
        elif not apr:
            flash('APR is required!')
        elif not name:
            flash('Asset Name is required!')
        else:
            messages.append({'Name': name, 'Amount': amount, 'APR': apr, 'start': start})
            pfs[num].add_asset(init_value=amount, start=start, apr=apr, name=name)
            return redirect(url_for('index'))

    return render_template('add_asset.html')

    # <a href="{{ url_for('add_budget') }}">Add Budget</a>
    # <a href="{{ url_for('add_investment') }}">Add Investment</a>
    # <a href="{{ url_for('add_loan') }}">Add Loan</a>

@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        elif not content:
            flash('Content is required!')
        else:
            messages.append({'title': title, 'content': content})
            return redirect(url_for('index'))

    return render_template('create.html')

if __name__ == "__main__":
    print(RTDIR)
    app.run(debug=True)
