import yfinance as yf


def usd(string):
    string = f"${string:,.2f}"
    # replace "$-" with "-$"
    if string.startswith('$-'):
        string = "-$" + string[2:]
    return string


def lookup(ticker_symbol):
    # Get the stock data
    stock = yf.Ticker(ticker_symbol)

    # Get historical market data
    hist = stock.history(period="5d")

    if len(hist) < 5:
        return None

    previous_close = hist['Close'].iloc[-2]
    current_close = hist['Close'].iloc[-1]

    # Calculate the price change
    price_change = current_close - previous_close
    percent_change = (price_change / previous_close) * 100

    return current_close, price_change, percent_change
