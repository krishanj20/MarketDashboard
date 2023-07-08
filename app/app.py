from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd
import pandas_datareader as pdr
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

dbc_css = ("https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.2/dbc.min.css")
app = Dash(__name__,
                external_stylesheets=[dbc.themes.LUX, dbc_css],
                meta_tags=[{'name':'viewport',
                            'content':'width=device-width,initial-scale=1.0'}],
                # use_pages=True,
                )


start = '2000-01-01'
tickers = ['REAINTRATREARAT10Y','T10YIE']
treasury_df = pdr.get_data_fred(tickers,start)
treasury_df.columns=['RealRate','10YBreakeven']
treasury_df.dropna(inplace=True)
# Changing format from 1st day of the month to last day of the month
treasury_df.index = treasury_df.index + pd.offsets.MonthEnd(0)


fig = go.FigureWidget()

fig.add_trace(go.Scatter(
    x=treasury_df.index,
    y=treasury_df['RealRate'] /100.0,
    name='Real Rate',
    yaxis='y1'  # Associate with the first Y-axis
))

fig.add_trace(go.Scatter(
    x=treasury_df.index,
    y=treasury_df['10YBreakeven'] /100.0,
    name='10Y Breakeven',
))

# Update layout with axis titles
fig.update_layout(
    title="Real Rate and 10Y Breakeven",
    yaxis=dict(
        title="Rate",
        tickformat=".2%"
    )
)

app.layout = html.Div([
    html.H1("US Interest Rates"),
    dcc.Graph(
        id="interest-rates-graph",
        figure={
            'data': [
                go.Scatter(
                    x=treasury_df.index,
                    y=treasury_df['RealRate'],
                    name='Real Rate',
                ),
                go.Scatter(
                    x=treasury_df.index,
                    y=treasury_df['10YBreakeven'],
                    name='10Y Breakeven',
                )
            ],
            'layout': go.Layout(
                title="Real Rate and 10Y Breakeven",
                yaxis=dict(
                    title="Rate (%)",
                    tickformat=".2%"
                ),
            )
        }
    )
])


if __name__ == '__main__':
    app.run(debug=True)