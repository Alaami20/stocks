import yfinance as yf
import pandas as pd
import numpy as np

tickers = ["AMZN", "TSLA", "NVDA", "GC=F"]
lookback_days = 60  # analyze last 60 trading days

recommendations = []

for ticker in tickers:
    asset = yf.Ticker(ticker)
    data = asset.history(period=f"{lookback_days}d").reset_index()
    
    if data.empty or 'Close' not in data.columns:
        continue
    
    data = data[['Date','Close']].dropna()
    
    # Calculate indicators
    data['Return'] = data['Close'].pct_change()
    momentum = data['Return'].mean() * 252  # annualized approx
    volatility = data['Return'].std() * np.sqrt(252)
    min_close = data['Close'].min()
    max_close = data['Close'].max()
    
    # Stoic score: reward upward trend, penalize high volatility
    score = momentum / (volatility + 1e-6)  # avoid divide by zero
    
    # Estimated future trade: buy near recent low, sell near recent high
    buy_price = min_close
    sell_price = max_close
    profit = sell_price - buy_price
    profit_pct = (profit / buy_price) * 100
    
    recommendations.append({
        "Ticker": ticker,
        "Score": round(score, 4),
        "Buy Price": round(buy_price,2),
        "Sell Price": round(sell_price,2),
        "Estimated Profit ($)": round(profit,2),
        "Estimated Profit (%)": round(profit_pct,2)
    })

# Sort by Stoic Score
recommendations.sort(key=lambda x: x["Score"], reverse=True)

# Show top recommendation
top = recommendations[0]
print("💡 Recommended Asset for Stoic Trade:")
print(f"Ticker: {top['Ticker']}")
print(f"Score: {top['Score']}")
print(f"Buy near: ${top['Buy Price']}")
print(f"Sell near: ${top['Sell Price']}")
print(f"Estimated Profit: ${top['Estimated Profit ($)']} ({top['Estimated Profit (%)']}%)")

# Show full table using pandas
df = pd.DataFrame(recommendations)
print("\n=== All Assets Stoic Scores ===")
print(df.to_string(index=False))
