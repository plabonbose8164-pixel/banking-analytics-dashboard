import pandas as pd

market = pd.read_excel(r"/Users/theplabone/python/clean_bank_data.xlsx")

fundamentals = pd.read_csv(r"/Users/theplabone/Downloads/fundamentals_indian_banks_fy25.csv")


merged = pd.merge(
    market,
    fundamentals,
    left_on="Bank",
    right_on="Bank_Name",
    how="left"
)

#print(merged.head())

merged.to_excel("final_bank_analytics_dataset.xlsx", index=False)

print("Final dataset saved successfully!")