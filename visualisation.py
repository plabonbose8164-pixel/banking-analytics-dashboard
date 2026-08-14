import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

banks = [
    "HDFCBANK.NS",
    "ICICIBANK.NS",
    "SBIN.NS",
    "AXISBANK.NS",
    "KOTAKBANK.NS",
    "IDFCFIRSTB.NS",
    "INDUSINDBK.NS",
    "AUBANK.NS",
    "BANKBARODA.NS",
    "FEDERALBNK.NS"
]

data = yf.download(
    banks,
    start="2021-01-01",
    end="2026-01-01",
    auto_adjust=True
)

tidy = (
    data
    .stack(level=1, future_stack=True)
    .reset_index()
)

tidy.columns = [
    "Date",
    "Bank",
    "Close",
    "High",
    "Low",
    "Open",
    "Volume"
]

# Sort data first
tidy = tidy.sort_values(["Bank", "Date"])
print(tidy.head())

tidy["Daily_Return"] = (
    tidy.groupby("Bank")["Close"]
        .pct_change()
        * 100
)

#Adding Parameters from existing DataFrame
#Adding Parameters from existing DataFrame

tidy["20_DMA"] = (
    tidy.groupby("Bank")["Close"]
        .transform(lambda x: x.rolling(window=20).mean())
)

tidy["50_DMA"] = (
    tidy.groupby("Bank")["Close"]
        .transform(lambda x: x.rolling(window=50).mean())
)

tidy["Trading_Range_%"] = (
    (tidy["High"] - tidy["Low"])
    / tidy["Close"]
) * 100

tidy["Volume_Change_%"] = (
    tidy.groupby("Bank")["Volume"]
        .pct_change()
        * 100
)

tidy["Volatility_20D"] = (
    tidy.groupby("Bank")["Daily_Return"]
        .transform(lambda x: x.rolling(20).std())
)

tidy["Cumulative_Return_%"] = (
    tidy.groupby("Bank")["Daily_Return"]
        .transform(lambda x: ((1 + x/100).cumprod() - 1) * 100)
)

tidy["52W_High"] = (
    tidy.groupby("Bank")["Close"]
        .transform(lambda x: x.rolling(252).max())
)

tidy["52W_Low"] = (
    tidy.groupby("Bank")["Close"]
        .transform(lambda x: x.rolling(252).min())
)

#business problems
#business problems

avg_return = (
    tidy.groupby("Bank")["Daily_Return"].mean().sort_values(ascending=False)
)

risk = (
    tidy.groupby("Bank")["Volatility_20D"]
        .mean()
        .sort_values(ascending=False)
)

avg_volume = (
    tidy.groupby("Bank")["Volume"].mean().sort_values(ascending=False))

highest_closing = (
    tidy.groupby("Bank")["Close"]
        .max()
        .sort_values(ascending=False)
)

#PLOTS & Visualization
#plot avg daily return

avg_return.plot(kind="bar", figsize=(10,5))
plt.title("Average Daily Return by Bank")
plt.ylabel("Return (%)")
plt.tight_layout()
plt.show()
#plot avg volatility
risk.plot(kind="bar", figsize=(10,5))
plt.title("Average 20-Day Volatility")
plt.ylabel("Volatility (%)")
plt.tight_layout()
plt.show()