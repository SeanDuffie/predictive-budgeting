"""_summary_
"""
import os

import bokeh.embed
import bokeh.plotting
import pandas as pd
import pandas_bokeh
from bokeh.models import ColumnDataSource, DatetimeTickFormatter
from bokeh.layouts import layout

RTDIR = os.path.dirname(__file__)

# create a pandas dataframe
df = pd.DataFrame({'date': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03']), 'value': [1, 2, 3]})

# create a Bokeh figure
# p = bokeh.plotting.figure(title="Line Plot", x_axis_label='Date', y_axis_label='Value')
p = bokeh.plotting.figure(title="Value")

# add a line renderer to the figure
p.line(x=df['date'], y=df['value'], line_width=2)

# bokeh.plotting.output_file()
# bokeh.plotting.save(p, filename=f"{RTDIR}/help")

html = bokeh.embed.file_html(p)
# print(f"{html=}\n\n\n")

# json = bokeh.embed.json_item(p)
# print(f"{json=}")

# show the figure
bokeh.plotting.show(p)
