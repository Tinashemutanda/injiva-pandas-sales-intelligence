import pandas as pd
import numpy as np


def calculate_financials(df):
    df = df.copy()

    df["Gross_Revenue"] = df["Quantity"] * df["Unit_Price"]

    df["Discount_Amount"] = df["Gross_Revenue"] * df["Discount_Percent"] / 100

    df["Net_Revenue"] = df["Gross_Revenue"] - df["Discount_Amount"]

    df["Total_Cost"] = df["Quantity"] * df["Unit_Cost"]

    df["Gross_Profit"] = df["Net_Revenue"] - df["Total_Cost"]

    df["Gross_Profit_Margin"] = df["Gross_Profit"] / df["Net_Revenue"].replace(0, np.nan) * 100

    return df

def aggregate_sales(df, group_column):
    summary = df.groupby(group_column).agg(
        Total_Revenue=("Net_Revenue", "sum"),
        Total_Profit=("Gross_Profit", "sum"),
        Units_Sold=("Quantity", "sum"),
        Transactions=("Transaction_ID", "count"),
        Average_Discount=("Discount_Percent", "mean")
    ).reset_index()

    summary["Profit_Margin"] = (
        summary["Total_Profit"] /
        summary["Total_Revenue"].replace(0, np.nan)
    ) * 100

    summary["Revenue_Contribution"] = (
        summary["Total_Revenue"] /
        df["Net_Revenue"].sum()
    ) * 100

    summary["Revenue_Rank"] = (
        summary["Total_Revenue"]
        .rank(method="dense", ascending=False)
        .astype(int)
    )

    return summary.sort_values(
        "Total_Revenue", ascending=False
    )


def generate_sales_summary(df):
    revenue = df["Net_Revenue"].sum()
    profit = df["Gross_Profit"].sum()

    return pd.DataFrame({
        "Total_Revenue": [revenue],
        "Total_Profit": [profit],
        "Total_Transactions": [len(df)],
        "Total_Units_Sold": [df["Quantity"].sum()],
        "Average_Transaction_Value": [
            df["Net_Revenue"].mean()
        ],
        "Overall_Profit_Margin": [
            profit / revenue * 100 if revenue else np.nan
        ]
    })