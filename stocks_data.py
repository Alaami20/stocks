import yfinance as yf
import pandas as pd

tickers = ["AAPL", "TSLA", "GOOGL", "AMZN", "MSFT", "NVDA", "GC=F"]
start_date = "2023-01-01"
end_date = "2025-01-01"

all_data = pd.DataFrame()

for ticker in tickers:
    print(f"Downloading {ticker}...")
    data = yf.download(ticker, start=start_date, end=end_date)
    if data.empty:
        print(f"No data for {ticker}")
        continue
    data['Ticker'] = ticker
    if 'Adj Close' not in data.columns:
        data['Adj Close'] = data['Close']
    # Only keep relevant columns
    data = data.reset_index()[["Date", "Ticker", "Open", "High", "Low", "Close", "Adj Close", "Volume"]]
    all_data = pd.concat([all_data, data])

# Reset index
all_data = all_data.reset_index(drop=True)

# Save CSV
all_data.to_csv("all_stocks_gold_tidy.csv", index=False)
print("✅ Downloaded all tickers in tidy format!")
  
df = pd.read_csv("all_stocks_gold_tidy.csv")

# List all unique tickers
print("All tickers in CSV:", df['Ticker'].unique())

# Count how many rows each ticker has
print(df['Ticker'].value_counts())



