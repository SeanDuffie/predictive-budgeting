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
df = pd.DataFrame({'date': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03']), 'value': [1, 2, 3]})

messages = [{'title': 'Message One',
             'content': 'Message One Content'},
            {'title': 'Message Two',
             'content': 'Message Two Content'}
            ]

@app.route("/")
def index():
    # TODO: Finish this: https://stackoverflow.com/questions/74286136/how-do-i-embed-a-bokeh-interactive-plot-in-a-flask-application
    # TODO: https://docs.bokeh.org/en/dev-3.0/docs/user_guide/embed.html
    p = bokeh.plotting.figure(title="Value")
    p.line(x=df['date'], y=df['value'], line_width=2)
    chart = bokeh.embed.file_html(p)
    
    empty_boxplot = bokeh.plotting.figure(
                plot_width=500,
                plot_height=450
            )
    script, div = bokeh.embed.components(empty_boxplot)
    
    return render_template("form.html", messages=messages, script=script, div=div)

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
