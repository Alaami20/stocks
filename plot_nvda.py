import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# Step 1: Download NVIDIA data
# -----------------------------
ticker = "NVDA"
nvda_ticker = yf.Ticker(ticker)
data = nvda_ticker.history(start="2023-01-01", end="2025-01-01")

if data.empty:
    print("❌ No data for NVIDIA!")
else:
    # Reset index
    data = data.reset_index()

    # Ensure Close and Adj Close exist
    if 'Close' not in data.columns:
        raise ValueError("No Close column found for NVIDIA!")
    if 'Adj Close' not in data.columns:
        data['Adj Close'] = data['Close']

    # Keep only relevant columns
    cols_to_keep = [col for col in ['Date','Close','Adj Close'] if col in data.columns]
    data = data[cols_to_keep]

    # Convert to numeric and datetime
    data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
    data['Close'] = pd.to_numeric(data['Close'], errors='coerce')
    data['Adj Close'] = pd.to_numeric(data['Adj Close'], errors='coerce')

    # Drop invalid rows
    data = data.dropna(subset=['Date','Close']).sort_values('Date')

    # -----------------------------
    # Compute moving averages and daily % change
    # -----------------------------
    data['MA20'] = data['Close'].rolling(20).mean()
    data['MA50'] = data['Close'].rolling(50).mean()
    data['Daily % Change'] = data['Close'].pct_change() * 100

    # -----------------------------
    # Plot Close + MA
    # -----------------------------
    plt.figure(figsize=(12,5))
    plt.plot(data['Date'], data['Close'], label='Close Price')
    plt.plot(data['Date'], data['MA20'], label='20-Day MA')
    plt.plot(data['Date'], data['MA50'], label='50-Day MA')
    plt.title('NVIDIA (NVDA) Price & Moving Averages')
    plt.xlabel('Date')
    plt.ylabel('Price USD')
    plt.legend()
    plt.show()

    # -----------------------------
    # Plot Daily % Change
    # -----------------------------
    plt.figure(figsize=(12,3))
    plt.plot(data['Date'], data['Daily % Change'], label='Daily % Change', color='orange')
    plt.axhline(0, color='black', linestyle='--', linewidth=1)
    plt.title('NVIDIA (NVDA) Daily % Change')
    plt.xlabel('Date')
    plt.ylabel('%')
    plt.legend()
    plt.show()
