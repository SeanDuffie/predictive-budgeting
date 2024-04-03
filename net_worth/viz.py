import pandas as pd
from bokeh.plotting import figure, show

# create a pandas dataframe
df = pd.DataFrame({'date': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03']), 'value': [1, 2, 3]})

# create a Bokeh figure
p = figure(title="Line Plot", x_axis_label='Date', y_axis_label='Value')

# add a line renderer to the figure
p.line(x=df['date'], y=df['value'], line_width=2)

# show the figure
show(p)
