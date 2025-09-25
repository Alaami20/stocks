import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV
df = pd.read_csv("all_stocks_gold_tidy.csv")

# Convert Date to datetime
df['Date'] = pd.to_datetime(df['Date'])

# List of tickers
tickers = df['Ticker'].unique()

# Plot Close price for all tickers
plt.figure(figsize=(14,7))
for ticker in tickers:
    data = df[df['Ticker'] == ticker]
    plt.plot(data['Date'], data['Close'], label=ticker)

plt.title('Stock & Gold Close Prices')
plt.xlabel('Date')
plt.ylabel('Price USD')
plt.legend()
plt.show()
