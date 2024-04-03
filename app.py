""" @file app.py
    @author Sean Duffie
    @brief Flask Framework to host the web user interface with the budgeting program
    
    This website allows a more convenient way for the user to utilize the budgeting tools.
    Additionally, this will display the Bokeh data visualization tools and potentially allow users
    to store and load data.
"""
import os

from flask import Flask, render_template

RTDIR = os.path.dirname(__file__)
app = Flask(
    import_name=__name__,
    static_folder=f"{RTDIR}/web/static",
    template_folder=f"{RTDIR}/web/templates"
)

@app.route("/")
def welcome():
    return render_template("form.html")

if __name__ == "__main__":
    print(RTDIR)
    # print(f"")
    app.run(debug=True)
