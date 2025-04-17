""" @file bk_stock_slider
    @author unknown, modified by Sean Duffie
    @brief This is an example 
"""
import os

import bokeh.embed
import numpy as np
import pandas as pd
from bokeh.layouts import column, layout
from bokeh.models import ColumnDataSource, DatetimeTickFormatter, RangeTool
from bokeh.plotting import figure, show


import bokeh.sampledata
bokeh.sampledata.download(progress=True)
from bokeh.sampledata.stocks import AAPL

RTDIR = os.path.dirname(__file__)

def norm_line():
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

def scroll_line():
    dates = np.array(AAPL['date'], dtype=np.datetime64)
    source = ColumnDataSource(data=dict(date=dates, close=AAPL['adj_close']))

    p = figure(height=300, width=800, tools="xpan", toolbar_location=None,
            x_axis_type="datetime", x_axis_location="below",
            background_fill_color="#efefef", x_range=(dates[1500], dates[2500]))

    p.line('date', 'close', source=source)
    p.yaxis.axis_label = 'Price'

    select = figure(title="Drag the middle and edges of the selection box to change the range above",
                    height=130, width=800, y_range=p.y_range,
                    x_axis_type="datetime", y_axis_type=None,
                    tools="", toolbar_location=None, background_fill_color="#efefef")

    range_tool = RangeTool(x_range=p.x_range)
    range_tool.overlay.fill_color = "navy"
    range_tool.overlay.fill_alpha = 0.2

    select.line('date', 'close', source=source)
    select.ygrid.grid_line_color = None
    select.add_tools(range_tool)

    show(column(p, select))

if __name__ == "__main__":
    scroll_line()
