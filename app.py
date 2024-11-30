import yfinance as yf
import dash
from dash import dcc, html, Input, Output, State, ctx
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.tools as tools
import pandas as pd
import numpy as np

# Initialize Dash app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Indicator Settings Modals
def create_indicator_modal(indicator_id, title, children):
    return dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle(title)),
            dbc.ModalBody(children),
            dbc.ModalFooter(
                dbc.Button("Close", id=f"{indicator_id}-modal-close", className="ms-auto", n_clicks=0)
            )
        ],
        id=f"{indicator_id}-modal",
        size="lg",
        centered=True,
        is_open=False,
    )

# EMA Settings Modal Content
ema_settings = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Label("EMA Period"),
            dbc.Input(
                id='ema-period', 
                type='number', 
                value=20, 
                min=1, 
                className="mb-2"
            )
        ], width=6),
        dbc.Col([
            dbc.Label("EMA Color"),
            dcc.Dropdown(
                id='ema-color',
                options=[
                    {'label': 'Red', 'value': '#FF0000'},
                    {'label': 'Blue', 'value': '#0000FF'},
                    {'label': 'Green', 'value': '#00FF00'},
                    {'label': 'Purple', 'value': '#800080'},
                ],
                value='#FF5733',
                clearable=False,
                className="mb-2"
            )
        ], width=6)
    ])
])

# MA Settings Modal Content
ma_settings = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Label("MA Period"),
            dbc.Input(
                id='ma-period', 
                type='number', 
                value=20, 
                min=1, 
                className="mb-2"
            )
        ], width=6),
        dbc.Col([
            dbc.Label("MA Color"),
            dcc.Dropdown(
                id='ma-color',
                options=[
                    {'label': 'Orange', 'value': '#FFA500'},
                    {'label': 'Blue', 'value': '#0000FF'},
                    {'label': 'Green', 'value': '#00FF00'},
                    {'label': 'Purple', 'value': '#800080'},
                ],
                value='#FFA500',
                clearable=False,
                className="mb-2"
            )
        ], width=6)
    ])
])

# Bollinger Bands Settings Modal Content
bb_settings = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Label("BB Period"),
            dbc.Input(
                id='bb-period', 
                type='number', 
                value=20, 
                min=1, 
                className="mb-2"
            )
        ], width=4),
        dbc.Col([
            dbc.Label("BB Multiplier"),
            dbc.Input(
                id='bb-multiplier', 
                type='number', 
                value=2, 
                min=1, 
                step=0.1, 
                className="mb-2"
            )
        ], width=4),
        dbc.Col([
            dbc.Label("BB Color"),
            dcc.Dropdown(
                id='bb-color',
                options=[
                    {'label': 'Blue', 'value': '#1E90FF'},
                    {'label': 'Red', 'value': '#FF0000'},
                    {'label': 'Green', 'value': '#00FF00'},
                    {'label': 'Purple', 'value': '#800080'},
                ],
                value='#1E90FF',
                clearable=False,
                className="mb-2"
            )
        ], width=4)
    ])
])

# RSI Settings Modal Content
rsi_settings = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Label("RSI Period"),
            dbc.Input(
                id='rsi-period', 
                type='number', 
                value=14, 
                min=1, 
                className="mb-2"
            )
        ], width=4),
        dbc.Col([
            dbc.Label("RSI MA Period"),
            dbc.Input(
                id='rsi-ma-period', 
                type='number', 
                value=5, 
                min=1, 
                className="mb-2"
            )
        ], width=4),
        dbc.Col([
            dbc.Label("RSI Color"),
            dcc.Dropdown(
                id='rsi-color',
                options=[
                    {'label': 'Green', 'value': '#33FF57'},
                    {'label': 'Blue', 'value': '#0000FF'},
                    {'label': 'Red', 'value': '#FF0000'},
                    {'label': 'Purple', 'value': '#800080'},
                ],
                value='#33FF57',
                clearable=False,
                className="mb-2"
            )
        ], width=4)
    ])
])

# MACD Settings Modal Content
macd_settings = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Label("MACD Fast Period"),
            dbc.Input(
                id='macd-fast', 
                type='number', 
                value=12, 
                min=1, 
                className="mb-2"
            )
        ], width=4),
        dbc.Col([
            dbc.Label("MACD Slow Period"),
            dbc.Input(
                id='macd-slow', 
                type='number', 
                value=26, 
                min=1, 
                className="mb-2"
            )
        ], width=4),
        dbc.Col([
            dbc.Label("Signal Line Period"),
            dbc.Input(
                id='macd-signal', 
                type='number', 
                value=9, 
                min=1, 
                className="mb-2"
            )
        ], width=4)
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Label("MACD Color"),
            dcc.Dropdown(
                id='macd-color',
                options=[
                    {'label': 'Green', 'value': '#33FF57'},
                    {'label': 'Blue', 'value': '#0000FF'},
                    {'label': 'Red', 'value': '#FF0000'},
                    {'label': 'Purple', 'value': '#800080'},
                ],
                value='#33FF57',
                clearable=False,
                className="mb-2"
            )
        ], width=12)
    ])
])

# App Layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Stock Visualizer", 
                        style={"fontSize": "24px", "margin": "10px 0"}, 
                        className="text-center"), width=12)
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Input(
                id='stock-name', 
                type='text', 
                placeholder='Enter stock ticker', 
                className="mb-2"
            )
        ], width=4),
        dbc.Col([
            dbc.Input(
                id='start-date', 
                type='text', 
                placeholder='YYYY-MM-DD (Start Date)', 
                className="mb-2"
            )
        ], width=4),
        dbc.Col([
            dbc.Input(
                id='end-date', 
                type='text', 
                placeholder='YYYY-MM-DD (End Date)', 
                className="mb-2"
            )
        ], width=4)
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            # Smaller button group with sm size
            dbc.ButtonGroup([
                dbc.Button("EMA", id="ema-toggle", color="primary", outline=True, size="sm"),
                dbc.Button("⚙️", id="ema-settings-btn", color="secondary", outline=True, size="sm"),
            ], className="me-1"),
            dbc.ButtonGroup([
                dbc.Button("MA", id="ma-toggle", color="primary", outline=True, size="sm"),
                dbc.Button("⚙️", id="ma-settings-btn", color="secondary", outline=True, size="sm"),
            ], className="me-1"),
            dbc.ButtonGroup([
                dbc.Button("BB", id="bb-toggle", color="primary", outline=True, size="sm"),
                dbc.Button("⚙️", id="bb-settings-btn", color="secondary", outline=True, size="sm"),
            ], className="me-1"),
            dbc.ButtonGroup([
                dbc.Button("RSI", id="rsi-toggle", color="primary", outline=True, size="sm"),
                dbc.Button("⚙️", id="rsi-settings-btn", color="secondary", outline=True, size="sm"),
            ], className="me-1"),
            dbc.ButtonGroup([
                dbc.Button("MACD", id="macd-toggle", color="primary", outline=True, size="sm"),
                dbc.Button("⚙️", id="macd-settings-btn", color="secondary", outline=True, size="sm"),
            ], className="me-1"),
            dbc.ButtonGroup([
                dbc.Button("Buy/Sell", id="buy-sell-toggle", color="success", outline=True, size="sm"),
            ], className="me-1")
        ], width=12, className="text-center mb-4")
    ]),
    
    dbc.Row([
        dbc.Col(dcc.Graph(id='candlestick-chart', style={'height': '90vh', 'width': '100%'}), width=12)
    ]),
    
    # Modals for each indicator
    create_indicator_modal('ema', 'EMA Settings', ema_settings),
    create_indicator_modal('ma', 'Moving Average Settings', ma_settings),
    create_indicator_modal('bb', 'Bollinger Bands Settings', bb_settings),
    create_indicator_modal('rsi', 'RSI Settings', rsi_settings),
    create_indicator_modal('macd', 'MACD Settings', macd_settings)
], fluid=True)

# Callback for modal toggles
def create_modal_callback(indicator):
    @app.callback(
        Output(f"{indicator}-modal", "is_open"),
        [Input(f"{indicator}-settings-btn", "n_clicks"),
         Input(f"{indicator}-modal-close", "n_clicks")],
        [State(f"{indicator}-modal", "is_open")]
    )
    def toggle_modal(n1, n2, is_open):
        if n1 or n2:
            return not is_open
        return is_open

# Create modal toggle callbacks for each indicator
for indicator in ['ema', 'ma', 'bb', 'rsi', 'macd']:
    create_modal_callback(indicator)

@app.callback(
    Output('candlestick-chart', 'figure'),
    [Input('stock-name', 'value'),
     Input('start-date', 'value'),
     Input('end-date', 'value'),
     Input('ema-toggle', 'n_clicks'),
     Input('ma-toggle', 'n_clicks'),
     Input('bb-toggle', 'n_clicks'),
     Input('rsi-toggle', 'n_clicks'),
     Input('macd-toggle', 'n_clicks'),
     Input('buy-sell-toggle', 'n_clicks'), 
     State('ema-period', 'value'),
     State('ema-color', 'value'),
     State('ma-period', 'value'),
     State('ma-color', 'value'),
     State('bb-period', 'value'),
     State('bb-multiplier', 'value'),
     State('bb-color', 'value'),
     State('rsi-period', 'value'),
     State('rsi-ma-period', 'value'),
     State('rsi-color', 'value'),
     State('macd-fast', 'value'),
     State('macd-slow', 'value'),
     State('macd-signal', 'value'),
     State('macd-color', 'value')]
)
def update_chart_with_buy_sell(stock_name, start_date, end_date, ema_clicks, ma_clicks, bb_clicks, rsi_clicks, macd_clicks, 
                               buy_sell_clicks, ema_period, ema_color, ma_period, ma_color, 
                               bb_period, bb_multiplier, bb_color, 
                               rsi_period, rsi_ma_period, rsi_color, 
                               macd_fast, macd_slow, macd_signal, macd_color):
    
    if not stock_name or not start_date or not end_date:
        return {}
    
    try:
        df = yf.download(stock_name, start=start_date, end=end_date).dropna()
        if df.empty:
            return {'layout': {'title': 'No data for the selected range.'}}
    except Exception as e:
        return {'layout': {'title': f'Error: {str(e)}'}}
    
    # Determine number of subplots
    subplot_rows = 1
    subplot_heights = [0.9]
    
    if (rsi_clicks and rsi_clicks % 2 != 0):
        subplot_rows += 1
        subplot_heights = [0.7, 0.3]
    
    if (macd_clicks and macd_clicks % 2 != 0):
        subplot_rows += 1
        subplot_heights = [0.6, 0.2, 0.2] if len(subplot_heights) == 1 else [0.7, 0.15, 0.15]
    
    # Create figure with dynamic subplots
    fig = tools.make_subplots(
        rows=subplot_rows, 
        cols=1, 
        shared_xaxes=True,
        vertical_spacing=0.05,
        row_heights=subplot_heights
    )
    
    # Candlestick chart (first subplot)
    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name='Candlestick',
        increasing_line_color='green',
        decreasing_line_color='red',
        increasing_line_width=1,
        decreasing_line_width=1
    ), row=1, col=1)

    # EMA
    if ema_clicks and ema_clicks % 2 != 0:
        df['EMA'] = df['Close'].ewm(span=ema_period).mean()
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['EMA'],
            mode='lines',
            name='EMA',
            line=dict(color=ema_color, width=2)
        ), row=1, col=1)

    # Moving Average (MA)
    if ma_clicks and ma_clicks % 2 != 0:
        df['MA'] = df['Close'].rolling(window=ma_period).mean()
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['MA'],
            mode='lines',
            name='Moving Average',
            line=dict(color=ma_color, width=2)
        ), row=1, col=1)
        
    # Bollinger Bands
    if bb_clicks and bb_clicks % 2 != 0:
        df['BB_Middle'] = df['Close'].rolling(window=bb_period).mean()
        df['BB_Upper'] = df['BB_Middle'] + bb_multiplier * df['Close'].rolling(window=bb_period).std()
        df['BB_Lower'] = df['BB_Middle'] - bb_multiplier * df['Close'].rolling(window=bb_period).std()

        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['BB_Upper'],
            mode='lines',
            name='BB Upper',
            line=dict(color=bb_color, dash='dash', width=1)
        ), row=1, col=1)

        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['BB_Lower'],
            mode='lines',
            name='BB Lower',
            line=dict(color=bb_color, dash='dash', width=1)
        ), row=1, col=1)

    # Determine dynamic rows for RSI and MACD
    rsi_row = 2 if (macd_clicks and macd_clicks % 2 != 0) else (2 if subplot_rows > 1 else 1)
    macd_row = 3 if (rsi_clicks and rsi_clicks % 2 != 0) and (macd_clicks and macd_clicks % 2 != 0) else (2 if subplot_rows > 1 else 1)

    # RSI with Moving Average
    if rsi_clicks and rsi_clicks % 2 != 0:
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(rsi_period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(rsi_period).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        df['RSI_MA'] = df['RSI'].rolling(rsi_ma_period).mean()

        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['RSI'],
            mode='lines',
            name='RSI',
            line=dict(color=rsi_color, width=1)
        ), row=rsi_row, col=1)
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['RSI_MA'],
            mode='lines',
            name='RSI Moving Avg',
            line=dict(color=rsi_color, dash='dot', width=1)
        ), row=rsi_row, col=1)
        
        # Add RSI threshold lines
        fig.add_trace(go.Scatter(
            x=df.index,
            y=[70] * len(df),
            mode='lines',
            name='RSI Overbought',
            line=dict(color='red', dash='dot', width=1)
        ), row=rsi_row, col=1)
        fig.add_trace(go.Scatter(
            x=df.index,
            y=[30] * len(df),
            mode='lines',
            name='RSI Oversold',
            line=dict(color='green', dash='dot', width=1)
        ), row=rsi_row, col=1)

    # MACD
    if macd_clicks and macd_clicks % 2 != 0:
        df['MACD'] = df['Close'].ewm(span=macd_fast).mean() - df['Close'].ewm(span=macd_slow).mean()
        df['MACD_Signal'] = df['MACD'].ewm(span=macd_signal).mean()

        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['MACD'],
            mode='lines',
            name='MACD',
            line=dict(color=macd_color, width=1)
        ), row=macd_row, col=1)
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['MACD_Signal'],
            mode='lines',
            name='MACD Signal',
            line=dict(color=macd_color, dash='dot', width=1)
        ), row=macd_row, col=1)
        
        # Add MACD histogram
        macd_histogram = df['MACD'] - df['MACD_Signal']
        fig.add_trace(go.Bar(
            x=df.index,
            y=macd_histogram,
            name='MACD Histogram',
            marker_color=np.where(macd_histogram >= 0, 'green', 'red')
        ), row=macd_row, col=1)

    # Update layout
    fig.update_layout(
        height=800,
        title=f'{stock_name.upper()} Chart with Indicators',
        title_x=0.5,
        margin=dict(l=40, r=40, t=60, b=40),
        template='plotly_dark',
        xaxis_rangeslider_visible=False,
        yaxis=dict(
            autorange=True
        )
    )

    # Add range slider at the bottom
    fig.update_xaxes(
        rangeslider=dict(
            visible=False,
            thickness=0.03
        ),
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=3, label="3m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ]),
            activecolor="#2c3e50",  # Active button color
            bgcolor="#34495e"       # Background color of the buttons
        ),
        row=1, 
        col=1
    )

    # Update y-axis titles
    fig.update_yaxes(title_text='Price', row=1, col=1)
    
    if rsi_clicks and rsi_clicks % 2 != 0:
        fig.update_yaxes(title_text='RSI', range=[0, 100], row=rsi_row, col=1)
    
    if macd_clicks and macd_clicks % 2 != 0:
        fig.update_yaxes(title_text='MACD', row=macd_row, col=1)

    fig.update_yaxes(
        autorange=True
    )

    plot_buy_sell = buy_sell_clicks and buy_sell_clicks % 2 != 0

    # Plot Buy and Sell signals
    buy_signal = []
    sell_signal = []

    if (bb_clicks and bb_clicks % 2 != 0) and (rsi_clicks and rsi_clicks % 2 != 0) and plot_buy_sell:
        buy_signal = (df['RSI'] < 30) & (df['Close'] < df['BB_Lower'])
        sell_signal = (df['RSI'] > 70) & (df['Close'] > df['BB_Upper'])

        # Plot Buy Signals
        fig.add_trace(go.Scatter(
            x=df.index[buy_signal],
            y=df['Close'][buy_signal],
            mode='markers',
            name='Buy Signal',
            marker=dict(
                symbol='triangle-up',
                color='green',
                size=10
            )
        ), row=1, col=1)

        # Plot Sell Signals
        fig.add_trace(go.Scatter(
            x=df.index[sell_signal],
            y=df['Close'][sell_signal],
            mode='markers',
            name='Sell Signal',
            marker=dict(
                symbol='triangle-down',
                color='red',
                size=10
            )
        ), row=1, col=1)
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
