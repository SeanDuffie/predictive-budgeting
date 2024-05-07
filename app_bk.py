''' An interactivate categorized chart based on a movie dataset.
This example shows the ability of Bokeh to create a dashboard with different
sorting options based on a given dataset.

'''
import datetime
import sqlite3 as sql
from os.path import dirname, join

import bokeh.io
import bokeh.layouts
import bokeh.models
import bokeh.plotting

from portfolio import Portfolio

axis_map = {
    "Tomato Meter": "Meter",
    "Numeric Rating": "numericRating",
    "Number of Reviews": "Reviews",
    "Box Office (dollars)": "BoxOffice",
    "Length (minutes)": "Runtime",
    "Year": "Year",
}

#################################
WIDTH = 1200
HEIGHT = 600
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
######################################

with open(join(dirname(__file__), "description.html")) as file:
    desc = bokeh.models.Div(text=file.read(), sizing_mode="stretch_width")

# Create Input controls
reviews = bokeh.models.Slider(title="Minimum number of reviews", value=80, start=10, end=300, step=10)
min_year = bokeh.models.Slider(title="Year released", start=1940, end=2014, value=1970, step=1)
max_year = bokeh.models.Slider(title="End Year released", start=1940, end=2014, value=2014, step=1)
oscars = bokeh.models.Slider(title="Minimum number of Oscar wins", start=0, end=4, value=0, step=1)
boxoffice = bokeh.models.Slider(title="Dollars at Box Office (millions)", start=0, end=800, value=0, step=1)
genre = bokeh.models.Select(title="Genre", value="All",
               options=open(join(dirname(__file__), 'genres.txt')).read().split())
director = bokeh.models.TextInput(title="Director name contains")
cast = bokeh.models.TextInput(title="Cast names contains")
x_axis = bokeh.models.Select(title="X Axis", options=sorted(axis_map.keys()), value="Tomato Meter")
y_axis = bokeh.models.Select(title="Y Axis", options=sorted(axis_map.keys()), value="Number of Reviews")

# Create Column Data Source that will be used by the plot
source = bokeh.models.ColumnDataSource(data=dict(x=[], y=[], color=[], title=[], year=[], revenue=[], alpha=[]))

TOOLTIPS=[
    ("Title", "@title"),
    ("Year", "@year"),
    ("$", "@revenue")
]

p = bokeh.plotting.figure(height=600, title="", toolbar_location=None, tooltips=TOOLTIPS, sizing_mode="stretch_width")
p.circle(x="x", y="y", source=source, size=7, color="color", line_color=None, fill_alpha="alpha")


def update():
    df = pfs[0].project_net(date=END)
    x_name = axis_map[x_axis.value]
    y_name = axis_map[y_axis.value]

    p.xaxis.axis_label = x_axis.value
    p.yaxis.axis_label = y_axis.value
    p.title.text = f"{len(df)} movies selected"
    source.data = dict(
        x=df[x_name],
        y=df[y_name],
        color=df["color"],
        title=df["Title"],
        year=df["Year"],
        revenue=df["revenue"],
        alpha=df["alpha"],
    )

controls = [reviews, boxoffice, genre, min_year, max_year, oscars, director, cast, x_axis, y_axis]
for control in controls:
    control.on_change('value', lambda attr, old, new: update())

inputs = bokeh.layouts.column(*controls, width=320, height=800)

layout = bokeh.layouts.column(desc, bokeh.layouts.row(inputs, p, sizing_mode="inherit"), sizing_mode="stretch_width", height=800)

update()  # initial load of the data

bokeh.io.curdoc().add_root(layout)
bokeh.io.curdoc().title = "Movies"
