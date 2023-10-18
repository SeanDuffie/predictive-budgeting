"""_summary_

Returns:
    _type_: _description_
"""
import json

import plotly.express as px
from dash import Dash, Input, Output, dcc, html

from database import Database

# df1 = px.data.stocks()
# fig1 = px.line(
#     df1,
#     x="date", y="MSFT", # replace with your own data source
#     title="MSFT Stock", height=325
# )

# df = Database()
df = Database(path="./database/Year End All Payment Methods100723.csv")
parent, child, sums = df.sum_cats()

data1 = dict(
    children = child,
    parents = parent,
    value = sums
)

fig1 = px.sunburst(
    df.d_frame,
    path=["Master Category", "Subcategory"],
    values="Amount"
)

# fig2 = px.line(
#     df.getDF(),
#     x=df.getDF()["Date"], y=df.getDF()["Amount"], # replace with your own data source
#     title="Credit Card", height=325
# )

# fig.show()
# fig1.show()
# fig2.show()

app = Dash(__name__)

app.layout = html.Div([
    html.H4('Displaying figure structure as JSON'),
    dcc.Graph(id="graph", figure=fig1),
])

# @app.callback(
#     Output("json_out", "children"),
#     Input("json_in", "figure"))
# def display_structure(fig_json):
#     """_summary_

#     Args:
#         fig_json (_type_): _description_

#     Returns:
#         _type_: _description_
#     """
#     return json.dumps(fig_json, indent=2)


if __name__ == "__main__":
    app.run_server(debug=True)
