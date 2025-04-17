""" @file stock.py
"""
import bokeh.sampledata
import pandas as pd
from bokeh.plotting import figure, show

try:
    from bokeh.sampledata.stocks import MSFT
except RuntimeError:
    bokeh.sampledata.download(progress=True)
    from bokeh.sampledata.stocks import MSFT

# Change the index to pick a different range of quarters
df = pd.DataFrame(MSFT)[0:180]
df["date"] = pd.to_datetime(df["date"])

inc = df.close > df.open
dec = df.open > df.close
w = 16*60*60*1000 # milliseconds

TOOLS = "pan,wheel_zoom,box_zoom,reset,save"

p = figure(x_axis_type="datetime", tools=TOOLS, width=1000, height=400,
           title="MSFT Candlestick", background_fill_color="#efefef")
p.xaxis.major_label_orientation = 0.8 # radians

p.segment(df.date, df.high, df.date, df.low, color="black")

p.vbar(df.date[dec], w, df.open[dec], df.close[dec], color="#eb3c40")
p.vbar(df.date[inc], w, df.open[inc], df.close[inc], fill_color="white",
       line_color="#49a3a3", line_width=2)

show(p)
