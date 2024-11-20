import dash
from dash import dcc, html
import pandas as pd
import requests
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import time


app = dash.Dash(__name__)


app.layout = html.Div([
    html.H1("Real-Time Stock Price Dashboard"),
    dcc.Dropdown(
        id='stock-dropdown',
        options=[
            {'label': 'Apple', 'value': 'AAPL'},
            {'label': 'Google', 'value': 'GOOGL'},
            {'label': 'Amazon', 'value': 'AMZN'}
        ],
        value='AAPL'
    ),
    dcc.Graph(id='live-graph'),
    dcc.Interval(
        id='interval-component',
        interval=10*1000,  # in milliseconds
        n_intervals=0
    )
])


def fetch_stock_data(symbol):
    api_key = 'M9115KTWJCQQVLIW'  # Replace with your Alpha Vantage API key
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=1min&apikey={api_key}'
    response = requests.get(url)
    data = response.json()
    return data


@app.callback(
    Output('live-graph', 'figure'),
    [Input('stock-dropdown', 'value'),
     Input('interval-component', 'n_intervals')]
)
def update_graph(selected_stock, n):
    data = fetch_stock_data(selected_stock)
    time_series = data['Time Series (1min)']

    # Prepare data for plotting
    times = list(time_series.keys())
    prices = [float(time_series[time]['1. open']) for time in times]

    # Create the figure
    figure = go.Figure()
    figure.add_trace(go.Scatter(x=times, y=prices, mode='lines+markers', name=selected_stock))
    figure.update_layout(title=f'Real-Time Stock Price for {selected_stock}', xaxis_title='Time', yaxis_title='Price (USD)')

    return figure


if __name__ == '__main__':
    app.run_server(debug=True)