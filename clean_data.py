import yfinance as yf
import pandas as pd

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

#tidy.to_excel("clean_bank_data.xlsx", index=False)
#print("Clean Excel file created successfully!")

# Sort data first
tidy = tidy.sort_values(["Bank", "Date"])
print(tidy.head())

tidy["Daily_Return"] = (
    tidy.groupby("Bank")["Close"]
        .pct_change()
        * 100
)

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

# avg_return = (
#     tidy.groupby("Bank")["Daily_Return"].mean().sort_values(ascending=False)
# )
# print(avg_return)

# risk = (
#     tidy.groupby("Bank")["Volatility_20D"]
#         .mean()
#         .sort_values(ascending=False)
# )

# avg_volume = (
#     tidy.groupby("Bank")["Volume"].mean().sort_values(descending = True)
# )
# print(avg_volume)

# highest_closing = (
#     tidy.groupby("Bank")["Close"]
#         .max()
#         .sort_values(ascending=False)
# )
# print(highest_closing)

print(
    tidy[
        ["Date","Bank","Close","Daily_Return","Volatility_20D", "Trading_Range_%"]
    ].head(60)
)

tidy.to_excel(
    "bank_analytics_dataset.xlsx",
    index=False
)
