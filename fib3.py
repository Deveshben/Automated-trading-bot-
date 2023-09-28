import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
import dash
from dash import html, dcc
from dash.dependencies import Input, Output

app = dash.Dash(__name__)
equity_details = pd.read_csv("EQUITY_L.csv")

app.layout = html.Div([
    html.H1("Fibonacci Retracement Analysis with Candlesticks"),
    dcc.Dropdown(
        id="select-share",
        options=[{'label': symbol, 'value': symbol} for symbol in equity_details.SYMBOL],
        value=equity_details.SYMBOL[0]
    ),
    dcc.Dropdown(
        id="select-timeframe",
        options=[
            {'label': '1 Day', 'value': '1d'},
            {'label': '1 Week', 'value': '1wk'},
            {'label': '1 Month', 'value': '1mo'},
        ],
        value='1mo'
    ),
    dcc.Graph(id='fibonacci-candlestick-chart', config={'scrollZoom': True}),
])

@app.callback(
    Output('fibonacci-candlestick-chart', 'figure'),
    [Input('select-share', 'value'),
     Input('select-timeframe', 'value')]
)
def update_fibonacci_candlestick_chart(selected_share, selected_timeframe):
    # Set a custom start date for fetching data for 1 day
    if selected_timeframe == '1d':
        start_date = '2021-01-01'
    else:
        start_date = '1969-01-01'

    data = yf.download(f"{selected_share}.NS", start=start_date, end=None, interval=selected_timeframe)

    # Calculate Fibonacci levels
    high = max(data['High'])
    low = min(data['Low'])
    fibonacci_levels = [low + (high - low) * ratio for ratio in [0.236, 0.382, 0.5, 0.618, 1.0]]

    # Create Fibonacci level lines
    fibonacci_lines = []
    for level in fibonacci_levels:
        fibonacci_lines.append(go.Scatter(
            x=data.index,
            y=[level] * len(data),
            mode='lines',
            name=f'Fib {int(level)}%',
            line=dict(width=1, dash='dash'),
        ))

    # Create candlestick chart
    candlestick = go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        name='Candlestick',
        increasing_line_color='green',
        decreasing_line_color='red',
        line=dict(width=1),
        opacity=1.0,
        hoverinfo='x+y+name',
        text=[f"Open: {open}<br>High: {high}<br>Low: {low}<br>Close: {close}" for open, high, low, close in
              zip(data['Open'], data['High'], data['Low'], data['Close'])]
    )

    y_axis_range = [data['Close'].min() * 0.95, data['Close'].max() * 1.05]
    layout = dict(
        title=f"{selected_share} Fibonacci Retracement Analysis ({selected_timeframe})",
        xaxis=dict(title='Date', rangeslider=dict(visible=True), type='date'),
        yaxis=dict(title='Price', fixedrange=False, range=y_axis_range),  # Enable vertical zoom with initial range
        showlegend=True,
        height=800,
        margin=dict(l=50, r=50, b=100, t=50),
    )

    return {'data': [candlestick] + fibonacci_lines, 'layout': layout}

if __name__ == '__main__':
    app.run_server(debug=True)
