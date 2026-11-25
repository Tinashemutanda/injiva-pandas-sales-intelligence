import pandas as pd

EXPECTED_SCHEMA = {
    "Transaction_ID": "string",
    "Date": "datetime64[ns]",
    "Product": "string",
    "Category": "string",
    "Quantity": "int64",
    "Unit_Price": "float64",
    "Unit_Cost": "float64",
    "Salesperson": "string",
    "City": "string",
    "Payment_Method": "string",
    "Discount_Percent": "float64"
}

MANDATORY_COLUMNS = list(EXPECTED_SCHEMA.keys())


def validate_schema(df, strict=False):
    """Validate mandatory columns and optionally data types."""

    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a Pandas DataFrame.")

    missing_columns = [
        column for column in MANDATORY_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing mandatory columns: {missing_columns}"
        )

    if df.columns.duplicated().any():
        raise ValueError("Duplicate column names detected.")

    if strict:
        for column, expected_type in EXPECTED_SCHEMA.items():
            actual_type = str(df[column].dtype)

            if actual_type != expected_type:
                raise TypeError(
                    f"{column}: expected {expected_type}, "
                    f"received {actual_type}"
                )

    return True