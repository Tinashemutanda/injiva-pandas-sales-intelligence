import pandas as pd
from .validation import (
    validate_schema,
    parse_date,
    PRODUCT_CATEGORIES,
    MANDATORY_COLUMNS
)


def standardise_products(df):
    df = df.copy()

    df["Product"] = (
        df["Product"]
        .astype("string")
        .str.strip()
        .str.title()
    )

    return df


def convert_dates(df):
    df = df.copy()

    df["Date"] = pd.to_datetime(
        df["Date"].apply(parse_date)
    )

    return df


def convert_numeric_types(df):
    df = df.copy()

    numeric_columns = [
        "Quantity",
        "Unit_Price",
        "Unit_Cost",
        "Discount_Percent"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column], errors="coerce"
        )

    return df


def clean_sales_data(df):
    validate_schema(df)

    original = df.copy(deep=True)
    cleaned = df.copy(deep=True)

    cleaned = standardise_products(cleaned)
    cleaned = convert_dates(cleaned)
    cleaned = convert_numeric_types(cleaned)

    reasons = pd.Series("", index=cleaned.index)

    def flag(mask, reason):
        reasons.loc[mask.fillna(True)] += reason + "; "

    flag(
        cleaned[MANDATORY_COLUMNS].isna().any(axis=1),
        "Missing or invalid mandatory value"
    )

    flag(
        cleaned["Quantity"] < 0,
        "Possible return requires verification"
    )

    flag(
        cleaned["Quantity"] == 0,
        "Zero quantity requires review"
    )

    flag(
        cleaned["Quantity"] % 1 != 0,
        "Quantity must be a whole number"
    )

    flag(
        cleaned["Unit_Price"].isna(),
        "Missing selling price"
    )

    flag(
        cleaned["Unit_Price"] <= 0,
        "Invalid selling price"
    )

    flag(
        cleaned["Unit_Cost"] <= 0,
        "Invalid unit cost"
    )

    flag(
        ~cleaned["Discount_Percent"].between(0, 100),
        "Invalid discount"
    )

    flag(
        cleaned["Transaction_ID"].duplicated(keep=False),
        "Duplicate transaction identifier"
    )

    flag(
        cleaned["Date"].isna(),
        "Invalid date"
    )

    expected_categories = cleaned["Product"].map(
        PRODUCT_CATEGORIES
    )

    flag(
        cleaned["Category"] != expected_categories,
        "Invalid product-category relationship"
    )

    rejected_mask = reasons != ""

    rejected = original.loc[rejected_mask].copy()

    rejected["Rejection_Reason"] = (
        reasons.loc[rejected_mask].str.rstrip("; ")
    )

    accepted = cleaned.loc[~rejected_mask].copy()

    string_columns = [
        "Transaction_ID",
        "Product",
        "Category",
        "Salesperson",
        "City",
        "Payment_Method"
    ]

    for column in string_columns:
        accepted[column] = accepted[column].astype("string")

    accepted["Quantity"] = accepted["Quantity"].astype("int64")

    for column in [
        "Unit_Price",
        "Unit_Cost",
        "Discount_Percent"
    ]:
        accepted[column] = accepted[column].astype("float64")

    accepted["Date"] = accepted["Date"].astype("datetime64[ns]")

    validate_schema(accepted, strict=True)

    assert accepted["Transaction_ID"].is_unique
    assert len(accepted) + len(rejected) == len(original)

    return accepted, rejected