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

def analyse_daily_sales(df):
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"])

    daily_sales = df.groupby("Date").agg(
        Daily_Revenue=("Net_Revenue", "sum"),
        Daily_Profit=("Gross_Profit", "sum"),
        Transaction_Count=("Transaction_ID", "count")
    ).sort_index()

    calendar = pd.date_range(
        start="2026-01-01",
        end="2026-01-31",
        freq="D"
    )

    daily_sales = daily_sales.reindex(calendar)
    daily_sales.index.name = "Date"

    daily_sales["Transaction_Count"] = (
        daily_sales["Transaction_Count"].fillna(0).astype(int)
    )

    daily_sales["Cumulative_Revenue"] = (
        daily_sales["Daily_Revenue"].fillna(0).cumsum()
    )

    daily_sales["Rolling_3_Day_Average"] = (
        daily_sales["Daily_Revenue"]
        .rolling(window=3, min_periods=3).mean()
    )

    return daily_sales.reset_index()

def classify_revenue(values):
    lower = values.quantile(1 / 3)
    upper = values.quantile(2 / 3)

    classifications = np.select(
        [
            values >= upper,
            values < lower
        ],
        ["High", "Low"],
        default="Medium"
    )

    return classifications, lower, upper
