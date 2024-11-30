# Stock Visualizer with Indicators

A Dash-based web application for visualizing stock market data with interactive candlestick charts and various technical indicators such as EMA, MA, Bollinger Bands, RSI, MACD. The app allows users to customize the indicators and visualize stock data over a specified date range.

![Ekran görüntüsü 2024-11-30 223225](https://github.com/user-attachments/assets/a5ab416f-6760-4af3-a36f-547f9b073564)

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Customization](#customization)
6. [Tech Stack](#tech-stack)
7. [Contributing](#contributing)
8. [License](#license)

## Overview

This project is a stock data visualizer built with **Dash** and **Plotly**, which allows users to:
- View real-time stock data by entering a stock ticker and a date range.
- Toggle technical indicators such as Exponential Moving Average (EMA), Moving Average (MA), Bollinger Bands (BB), Relative Strength Index (RSI), and Moving Average Convergence Divergence (MACD).
- Customize settings for each indicator, including period and color.
- View buy/sell signals based on indicator conditions like RSI and Bollinger Bands.

The app uses the Yahoo Finance API (`yfinance` library) to fetch the stock data and allows interactive visualization through a candlestick chart.

## Features

- **Candlestick chart** for stock prices.
- **EMA, MA, Bollinger Bands, RSI, MACD** indicators with adjustable settings.
- **Responsive design** with Bootstrap.
- **Buy/Sell signal generation** based on RSI and Bollinger Bands criteria.
- **Date range picker** for historical stock data.
- **Interactive modals** to customize indicator settings.
- **Multi-indicator display** with dynamic layout adjustment based on active indicators.

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Step-by-step guide

1. Clone the repository to your local machine:
    ```bash
    git clone https://github.com/yourusername/stock-visualizer.git
    ```

2. Navigate to the project directory:
    ```bash
    cd stock-visualizer
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Start the Dash app:
    ```bash
    python app.py
    ```

5. Open your web browser and go to `http://127.0.0.1:8050` to view the app.

## Usage

- Enter a stock ticker symbol (e.g., "AAPL" for Apple) in the stock name input field.
- Set the start and end dates to define the range of data you want to visualize (e.g., "2023-01-01" to "2024-01-01").
- Toggle any of the technical indicators (EMA, MA, Bollinger Bands, RSI, MACD) to see them on the chart.
- Click the ⚙️ button to access settings for each indicator and customize the period, color, etc.
- View buy/sell signals based on the selected indicators.

## Customization

### Indicator Settings
Each indicator (EMA, MA, Bollinger Bands, RSI, MACD) has its own modal for adjusting:
- **Period**: The number of days over which the indicator is calculated.
- **Color**: Choose a color for the indicator's line to match your preference.

### Buy/Sell Signals
Buy and sell signals are generated based on two conditions:
- **Buy Signal**: When RSI < 30 and price is below the lower Bollinger Band.
- **Sell Signal**: When RSI > 70 and price is above the upper Bollinger Band.

### Adjusting the Date Range
You can define the start and end dates for fetching historical stock data. The available range can be selected directly on the chart with buttons like "1m", "3m", "1y", etc.

## Tech Stack

- **Dash**: Web framework for building analytical web applications.
- **Plotly**: Graphing library for creating interactive plots.
- **yfinance**: Library for downloading historical stock data from Yahoo Finance.
- **Pandas**: Data manipulation and analysis library.
- **Bootstrap**: Frontend framework for responsive design.
- **Python**: Programming language for the app.

## Contributing

If you would like to contribute to the project:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Push to your fork and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
