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

from flask import Flask, flash, redirect, render_template, request, url_for

RTDIR = os.path.dirname(__file__)
app = Flask(
    import_name=__name__,
    static_folder=f"{RTDIR}/web/static",
    template_folder=f"{RTDIR}/web/templates"
)
app.config['SECRET_KEY'] = '1d2e3382586f37723ba8aad13ece71d521e2b6fd1d0e7407'

messages = [{'title': 'Message One',
             'content': 'Message One Content'},
            {'title': 'Message Two',
             'content': 'Message Two Content'}
            ]

@app.route("/")
def index():
    return render_template("form.html", messages=messages)

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
