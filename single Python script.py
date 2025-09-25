import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# -----------------------------
# List of assets
# -----------------------------
tickers = ["AMZN", "TSLA", "NVDA", "GC=F"]
start_date = "2023-01-01"
end_date = "2025-01-01"

best_trades = {}

for ticker in tickers:
    print(f"Processing {ticker}...")
    asset = yf.Ticker(ticker)
    data = asset.history(start=start_date, end=end_date).reset_index()
    
    # Ensure Close column exists
    if 'Close' not in data.columns:
        print(f"⚠️ No Close data for {ticker}, skipping.")
        continue
    
    # Keep only Date and Close
    data = data[['Date','Close']].dropna()
    
    # -----------------------------
    # Compute best trade (max profit)
    # -----------------------------
    min_price = np.inf
    max_profit = 0
    buy_date = None
    sell_date = None
    
    for i, row in data.iterrows():
        price = row['Close']
        date = row['Date']
        if price < min_price:
            min_price = price
            potential_buy_date = date
        profit = price - min_price
        if profit > max_profit:
            max_profit = profit
            buy_date = potential_buy_date
            sell_date = date
    
    best_trades[ticker] = {
        'data': data,
        'buy_date': buy_date,
        'sell_date': sell_date,
        'buy_price': min_price,
        'sell_price': min_price + max_profit,
        'profit': max_profit
    }

# -----------------------------
# Plot all assets with best trades
# -----------------------------
fig, axes = plt.subplots(len(best_trades), 1, figsize=(12, 4*len(best_trades)), sharex=False)

if len(best_trades) == 1:
    axes = [axes]  # make iterable

for ax, (ticker, info) in zip(axes, best_trades.items()):
    data = info['data']
    ax.plot(data['Date'], data['Close'], label='Close Price')
    ax.scatter(info['buy_date'], info['buy_price'], color='green', marker='^', s=150, label='Buy')
    ax.scatter(info['sell_date'], info['sell_price'], color='red', marker='v', s=150, label='Sell')
    ax.set_title(f"{ticker} - Best Trade: Buy {info['buy_date'].date()} (${info['buy_price']:.2f}), "
                 f"Sell {info['sell_date'].date()} (${info['sell_price']:.2f}), Profit ${info['profit']:.2f}")
    ax.set_xlabel('Date')
    ax.set_ylabel('Price USD')
    ax.legend()

plt.tight_layout()
plt.show()
