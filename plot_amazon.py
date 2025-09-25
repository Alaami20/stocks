import pandas as pd
import matplotlib.pyplot as plt

# Load CSV
df = pd.read_csv("amazon.csv")  # use the CSV we just fixed

# Ensure Date column is datetime
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# Convert numeric columns to float
numeric_cols = ['Open','High','Low','Close','Adj Close','Volume']
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Drop rows with missing Date or Close
df = df.dropna(subset=['Date','Close']).sort_values('Date')

# Calculate moving averages
df['MA20'] = df['Close'].rolling(window=20).mean()
df['MA50'] = df['Close'].rolling(window=50).mean()

# Calculate daily % change
df['Daily % Change'] = df['Close'].pct_change() * 100

# -------------------------------
# Plot Close Price + MAs
# -------------------------------
plt.figure(figsize=(12,5))
plt.plot(df['Date'], df['Close'], label='Close Price')
plt.plot(df['Date'], df['MA20'], label='20-Day MA')
plt.plot(df['Date'], df['MA50'], label='50-Day MA')
plt.title('Amazon (AMZN) Price & Moving Averages')
plt.xlabel('Date')
plt.ylabel('Price USD')
plt.legend()
plt.show()

# -------------------------------
# Plot Daily % Change
# -------------------------------
plt.figure(figsize=(12,3))
plt.plot(df['Date'], df['Daily % Change'], label='Daily % Change', color='orange')
plt.axhline(0, color='black', linestyle='--', linewidth=1)
plt.title('Amazon (AMZN) Daily % Change')
plt.xlabel('Date')
plt.ylabel('%')
plt.legend()
plt.show()
