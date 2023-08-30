from dash import Dash, dcc, html, Input, Output
from database import Database
import plotly.express as px
import json

df1 = px.data.stocks()
fig1 = px.line(
    df1,
    x="date", y="MSFT", # replace with your own data source
    title="MSFT Stock", height=325
)

df2 = Database().getDF()
fig2 = px.line(
    df2,
    x=df2["Date"], y=df2["Amount"], # replace with your own data source
    title="Credit Card", height=325
)

# fig1.show()
# fig2.show()

app = Dash(__name__)

app.layout = html.Div([
    html.H4('Displaying figure structure as JSON'),
    dcc.Graph(id="graph", figure=fig2),
    dcc.Clipboard(target_id="structure"),
    html.Pre(
        id='structure',
        style={
            'border': 'thin lightgrey solid', 
            'overflowY': 'scroll',
            'height': '275px'
        }
    ),
])

@app.callback(
    Output("figure-structure-x-structure", "children"), 
    Input("figure-structure-x-graph", "figure"))
def display_structure(fig_json):
    return json.dumps(fig_json, indent=2)


if __name__ == "__main__":
    app.run_server(debug=True)
