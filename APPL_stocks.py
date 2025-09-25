import pandas as pd
import matplotlib.pyplot as plt

# Load CSV
df = pd.read_csv("all_stocks_gold_tidy.csv")

# Convert Date to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Convert numeric columns to float
numeric_cols = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')  # invalid parsing becomes NaN

# Drop rows with NaN in 'Close' to avoid errors
df = df.dropna(subset=['Close'])

# Get all tickers
tickers = df['Ticker'].unique()
print(f"Detected tickers: {tickers}")

# Loop through tickers and plot
for ticker in tickers:
    data = df[df['Ticker'] == ticker].sort_values('Date')

    # Calculate moving averages
    data['MA20'] = data['Close'].rolling(window=20).mean()
    data['MA50'] = data['Close'].rolling(window=50).mean()

    # Calculate daily percent change
    data['Daily % Change'] = data['Close'].pct_change() * 100

    # Plot Close Price + MA
    plt.figure(figsize=(12,5))
    plt.plot(data['Date'], data['Close'], label='Close Price')
    plt.plot(data['Date'], data['MA20'], label='20-Day MA')
    plt.plot(data['Date'], data['MA50'], label='50-Day MA')
    plt.title(f'{ticker} Price & Moving Averages')
    plt.xlabel('Date')
    plt.ylabel('Price USD')
    plt.legend()
    plt.show()

    # Plot Daily % Change
    plt.figure(figsize=(12,3))
    plt.plot(data['Date'], data['Daily % Change'], label='Daily % Change', color='orange')
    plt.axhline(0, color='black', linestyle='--', linewidth=1)
    plt.title(f'{ticker} Daily % Change')
    plt.xlabel('Date')
    plt.ylabel('%')
    plt.legend()
    plt.show()
