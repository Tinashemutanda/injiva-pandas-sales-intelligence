from pathlib import Path

import pandas as pd
import numpy as np

from src.sales_data import sales_data

from src.validation import (
    validate_schema,
    assess_data_quality
)

from src.cleaning import clean_sales_data

from src.analytics import (
    calculate_financials,
    aggregate_sales,
    generate_sales_summary,
    analyse_daily_sales,
    classify_revenue
)


# 1. Construct DataFrame
def construct_dataframe():
    return pd.DataFrame(sales_data)


# 2. Validate source data
def validate_data(df):
    validate_schema(df)
    return df


# 3. Assess data quality
def investigate_quality(df):
    return assess_data_quality(df)


# 4. Clean sales data
def process_cleaning(df):
    accepted, rejected = clean_sales_data(df)

    validate_schema(accepted, strict=True)

    assert len(df) == len(accepted) + len(rejected)

    return accepted, rejected


# 5. Financial transformation
def process_financials(df):
    return calculate_financials(df)


# 6. Sales aggregation
def generate_aggregations(df):
    return {
        "sales_summary": generate_sales_summary(df),

        "product_performance": aggregate_sales(
            df, "Product"
        ),

        "category_performance": aggregate_sales(
            df, "Category"
        ),

        "city_performance": aggregate_sales(
            df, "City"
        ),

        "salesperson_performance": aggregate_sales(
            df, "Salesperson"
        ),

        "payment_performance": aggregate_sales(
            df, "Payment_Method"
        )
    }


# 7. Performance analysis
def analyse_performance(df):
    segmented = df.copy()

    classifications, lower, upper = classify_revenue(
        segmented["Net_Revenue"]
    )

    segmented["Transaction_Segment"] = classifications

    segment_summary = (
        segmented.groupby("Transaction_Segment")
        .agg(
            Transactions=("Transaction_ID", "count"),
            Total_Revenue=("Net_Revenue", "sum"),
            Total_Profit=("Gross_Profit", "sum")
        )
        .reset_index()
    )

    segment_summary["Revenue_Contribution"] = (
        segment_summary["Total_Revenue"] /
        segmented["Net_Revenue"].sum()
    ) * 100

    daily_sales = analyse_daily_sales(df)

    city_category = (
        df.groupby(["City", "Category"])
        .agg(
            Total_Revenue=("Net_Revenue", "sum"),
            Total_Profit=("Gross_Profit", "sum"),
            Transactions=("Transaction_ID", "count")
        )
        .reset_index()
    )

    return {
        "transaction_segmentation": segmented,
        "segment_summary": segment_summary,
        "daily_sales": daily_sales,
        "city_category_summary": city_category
    }


# 8. Financial validation
def validate_financial_totals(df, reports):
    total_revenue = df["Net_Revenue"].sum()
    total_profit = df["Gross_Profit"].sum()

    for name in [
        "product_performance",
        "category_performance",
        "city_performance",
        "salesperson_performance"
    ]:
        report = reports[name]

        assert np.isclose(
            report["Total_Revenue"].sum(),
            total_revenue
        )

        assert np.isclose(
            report["Total_Profit"].sum(),
            total_profit
        )

    assert df["Transaction_ID"].is_unique

    assert (df["Quantity"] > 0).all()

    assert (df["Unit_Price"] > 0).all()

    print("Financial validation passed.")


# 9. Export reports
def export_reports(reports, output_directory):
    output_directory = Path(output_directory)

    output_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    for name, dataframe in reports.items():
        dataframe.to_csv(
            output_directory / f"{name}.csv",
            index=False
        )

        print(f"Exported: {name}.csv")


# 10. Main pipeline
def run_pipeline(output_directory=None):

    if output_directory is None:
        output_directory = (
            Path(__file__).resolve().parent.parent
            / "data"
        )

    print("Starting sales processing pipeline...")

    original_df = construct_dataframe()

    validate_data(original_df)

    quality_report = investigate_quality(original_df)

    cleaned_df, rejected_df = process_cleaning(
        original_df
    )

    financial_df = process_financials(cleaned_df)

    reports = generate_aggregations(financial_df)

    performance_reports = analyse_performance(
        financial_df
    )

    reports.update(performance_reports)

    quality_report = quality_report.copy()

    quality_report["Resolution_Status"] = np.where(
        quality_report["Transaction_ID"].isin(
            rejected_df["Transaction_ID"]
        ),
        "Rejected - Pending Review",
        "Resolved"
    )

    reports["cleaned_sales"] = financial_df
    reports["rejected_records"] = rejected_df
    reports["data_quality_report"] = quality_report

    reports["cleaning_summary"] = pd.DataFrame({
        "Metric": [
            "Original Transactions",
            "Accepted Transactions",
            "Rejected Transactions",
            "Acceptance Rate (%)"
        ],
        "Value": [
            len(original_df),
            len(cleaned_df),
            len(rejected_df),
            len(cleaned_df) / len(original_df) * 100
        ]
    })

    validate_financial_totals(financial_df, reports)

    export_reports(reports, output_directory)

    print("\nPIPELINE COMPLETED SUCCESSFULLY")
    print("Original records:", len(original_df))
    print("Accepted records:", len(cleaned_df))
    print("Rejected records:", len(rejected_df))

    print(
        "Total Net Revenue:",
        round(financial_df["Net_Revenue"].sum(), 2)
    )

    print(
        "Total Gross Profit:",
        round(financial_df["Gross_Profit"].sum(), 2)
    )

    return reports


if __name__ == "__main__":
    run_pipeline()