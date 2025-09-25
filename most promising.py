import yfinance as yf
import pandas as pd
import numpy as np

# Assets
tickers = ["AMZN", "TSLA", "NVDA", "GC=F"]
lookback_days = 60  # recent period to analyze

best_asset = None
best_profit = 0
best_trade = {}

for ticker in tickers:
    asset = yf.Ticker(ticker)
    data = asset.history(period=f"{lookback_days}d").reset_index()
    
    if 'Close' not in data.columns or data.empty:
        continue
    
    data = data[['Date','Close']].dropna()
    
    # Find best trade in this recent period
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
    
    profit_pct = (max_profit / min_price) * 100 if min_price > 0 else 0
    
    if max_profit > best_profit:
        best_profit = max_profit
        best_asset = ticker
        best_trade = {
            "Buy Date": buy_date.date(),
            "Buy Price": round(min_price, 2),
            "Sell Date": sell_date.date(),
            "Sell Price": round(min_price + max_profit, 2),
            "Profit ($)": round(max_profit, 2),
            "Profit (%)": round(profit_pct, 2)
        }

# Display recommendation
if best_asset:
    print(f"💹 Recommended Asset to Trade Now: {best_asset}")
    print("=== Best Trade in Last 60 Days ===")
    for key, value in best_trade.items():
        print(f"{key}: {value}")
else:
    print("⚠️ No valid data found to suggest a trade.")
