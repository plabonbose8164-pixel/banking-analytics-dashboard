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

print(data.head())

data.to_excel("bank_stock_data.xlsx")

print("Excel file created successfully!")