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

import bokeh.embed
import bokeh.plotting
import pandas as pd
from flask import Flask, flash, redirect, render_template, request, url_for

# from portfolio import Portfolio

RTDIR = os.path.dirname(__file__)
app = Flask(
    import_name=__name__,
    static_folder=f"{RTDIR}/web/static",
    template_folder=f"{RTDIR}/web/templates"
)
app.config['SECRET_KEY'] = '1d2e3382586f37723ba8aad13ece71d521e2b6fd1d0e7407'

# portfolio = Portfolio("net_worth.db")
df = pd.DataFrame({'Date': pd.to_datetime(['2021-01-01', '2022-01-01', '2023-01-01']), 'Net': [1, 2, 3]})

messages = [{'title': 'Message One',
             'content': 'Message One Content'},
            {'title': 'Message Two',
             'content': 'Message Two Content'}
            ]

@app.route("/")
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

    plot.circle([1,2], [3,4])
    plot.line(x=df['Date'], y=df['Net'], legend_label="Net", line_width=8, line_color='green')

    plot.legend.title = "Categories"
    plot.legend.location = "top_left"

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
    # print(f"")
    app.run(debug=True)
