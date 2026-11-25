import pandas as pd
import numpy as np
import pytest

from src.sales_data import sales_data
from src.validation import validate_schema
from src.cleaning import clean_sales_data
from src.analytics import calculate_financials, aggregate_sales


@pytest.fixture
def original_data():
    return pd.DataFrame(sales_data)


@pytest.fixture
def cleaned_data(original_data):
    accepted, rejected = clean_sales_data(original_data)
    return accepted


@pytest.fixture
def financial_data(cleaned_data):
    return calculate_financials(cleaned_data)


# Test 1: Mandatory columns
def test_mandatory_columns(cleaned_data):
    required_columns = [
        "Transaction_ID",
        "Date",
        "Product",
        "Category",
        "Quantity",
        "Unit_Price",
        "Unit_Cost",
        "Salesperson",
        "City",
        "Payment_Method",
        "Discount_Percent"
    ]

    assert set(required_columns).issubset(
        cleaned_data.columns
    )


# Test 2: Unique transaction identifiers
def test_unique_transaction_ids(cleaned_data):
    assert cleaned_data["Transaction_ID"].is_unique


# Test 3: Valid quantities
def test_valid_quantities(cleaned_data):
    assert (cleaned_data["Quantity"] > 0).all()


# Test 4: Valid unit prices
def test_valid_unit_prices(cleaned_data):
    assert cleaned_data["Unit_Price"].notna().all()
    assert (cleaned_data["Unit_Price"] > 0).all()


# Test 5: Valid discounts
def test_valid_discounts(cleaned_data):
    assert cleaned_data["Discount_Percent"].between(
        0, 100
    ).all()


# Test 6: Correct financial calculations
def test_revenue_calculation():
    sample = pd.DataFrame({
        "Quantity": [2],
        "Unit_Price": [100.0],
        "Unit_Cost": [60.0],
        "Discount_Percent": [10.0]
    })

    result = calculate_financials(sample)

    assert result["Gross_Revenue"].iloc[0] == pytest.approx(200)
    assert result["Discount_Amount"].iloc[0] == pytest.approx(20)
    assert result["Net_Revenue"].iloc[0] == pytest.approx(180)


# Test 7: Correct gross profit
def test_gross_profit_calculation():
    sample = pd.DataFrame({
        "Quantity": [2],
        "Unit_Price": [100.0],
        "Unit_Cost": [60.0],
        "Discount_Percent": [10.0]
    })

    result = calculate_financials(sample)

    assert result["Total_Cost"].iloc[0] == pytest.approx(120)
    assert result["Gross_Profit"].iloc[0] == pytest.approx(60)
    assert result["Gross_Profit_Margin"].iloc[0] == pytest.approx(
        33.333333
    )


# Test 8: Valid dates
def test_valid_dates(cleaned_data):
    assert pd.api.types.is_datetime64_any_dtype(
        cleaned_data["Date"]
    )

    assert cleaned_data["Date"].notna().all()


# Test 9: Successful DataFrame merge
def test_successful_merge(financial_data):
    reference = pd.DataFrame({
        "Product": [
            "Laptop", "Smartphone", "Keyboard",
            "Monitor", "Printer", "Mouse"
        ],
        "Product_Code": [
            "P001", "P002", "P003",
            "P004", "P005", "P006"
        ]
    })

    merged = financial_data.merge(
        reference,
        on="Product",
        how="left",
        validate="many_to_one"
    )

    assert len(merged) == len(financial_data)
    assert merged["Transaction_ID"].is_unique
    assert merged["Product_Code"].notna().all()

    assert np.isclose(
        merged["Net_Revenue"].sum(),
        financial_data["Net_Revenue"].sum()
    )


# Test 10: Financial reconciliation
def test_financial_reconciliation(financial_data):
    for column in [
        "City", "Product", "Category", "Salesperson"
    ]:
        summary = aggregate_sales(
            financial_data, column
        )

        assert np.isclose(
            summary["Total_Revenue"].sum(),
            financial_data["Net_Revenue"].sum()
        )

        assert np.isclose(
            summary["Total_Profit"].sum(),
            financial_data["Gross_Profit"].sum()
        )


# Test 11: Deliberately invalid transaction
def test_invalid_transaction(original_data):
    invalid_record = original_data.iloc[[0]].copy()

    invalid_record["Transaction_ID"] = "TX999"
    invalid_record["Quantity"] = -10

    test_data = pd.concat(
        [original_data, invalid_record],
        ignore_index=True
    )

    accepted, rejected = clean_sales_data(test_data)

    assert "TX999" not in accepted["Transaction_ID"].values
    assert "TX999" in rejected["Transaction_ID"].values


# Test 12: Cleaning record reconciliation
def test_cleaning_reconciliation(original_data):
    accepted, rejected = clean_sales_data(original_data)

    assert len(original_data) == 20
    assert len(accepted) == 17
    assert len(rejected) == 3

    assert len(original_data) == len(accepted) + len(rejected)