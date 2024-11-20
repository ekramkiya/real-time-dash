import dash
from dash import dcc, html
import requests
import plotly.graph_objs as go
from dash.dependencies import Input, Output

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
    time_series = data.get('Time Series (1min)', {})

    if not time_series:
        print("No data found for the given stock.")
        return go.Figure()  # Return an empty figure if no data

    # Prepare data for plotting
    times = list(time_series.keys())
    times.sort()  # Ensure times are sorted
    prices = [float(time_series[time]['1. open']) for time in times]

    # Create the figure
    figure = go.Figure()
    figure.add_trace(go.Scatter(x=times, y=prices, mode='lines+markers', name=selected_stock))
    
    # Update layout for dark mode
    figure.update_layout(
        template='plotly_dark',
        title=f'Real-Time Stock Price for {selected_stock}',
        xaxis_title='Time',
        yaxis_title='Price (USD)',
        plot_bgcolor='#1e1e1e',
        paper_bgcolor='#1e1e1e',
        font=dict(color='white')
    )

    return figure

if __name__ == '__main__':
    app.run_server(debug=True)