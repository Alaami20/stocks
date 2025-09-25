import yfinance as yf
import pandas as pd
import numpy as np

# List of assets
tickers = ["AMZN", "TSLA", "NVDA", "GC=F"]
start_date = "2023-01-01"
end_date = "2025-01-01"

stats_list = []

for ticker in tickers:
    asset = yf.Ticker(ticker)
    data = asset.history(start=start_date, end=end_date).reset_index()
    
    if 'Close' not in data.columns:
        print(f"⚠️ No Close data for {ticker}, skipping.")
        continue
    
    data = data[['Date','Close']].dropna()
    
    # Initialize
    min_price = np.inf
    max_profit = 0
    buy_date = None
    sell_date = None
    
    # Find best trade
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
    
    # Profit percentage
    profit_pct = (max_profit / min_price) * 100 if min_price > 0 else 0
    
    stats_list.append({
        "Ticker": ticker,
        "Buy Date": buy_date.date(),
        "Buy Price": round(min_price, 2),
        "Sell Date": sell_date.date(),
        "Sell Price": round(min_price + max_profit, 2),
        "Profit ($)": round(max_profit, 2),
        "Profit (%)": round(profit_pct, 2)
    })

# Convert to DataFrame
stats_df = pd.DataFrame(stats_list)

# Display in a clear table
print("=== Best Trade Summary ===")
print(stats_df.to_string(index=False))
