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
PRODUCT_CATEGORIES = {
    "Laptop": "Computers",
    "Monitor": "Computers",
    "Smartphone": "Mobile",
    "Keyboard": "Accessories",
    "Mouse": "Accessories",
    "Printer": "Office Equipment"
}


def parse_date(value):
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
        try:
            return pd.to_datetime(value, format=fmt)
        except (ValueError, TypeError):
            continue

    return pd.NaT


def assess_data_quality(df):
    validate_schema(df)

    issues = []

    def add_issue(row, column, description, severity, action):
        issues.append({
            "Transaction_ID": row["Transaction_ID"],
            "Affected_Column": column,
            "Original_Value": row[column],
            "Issue_Description": description,
            "Severity": severity,
            "Recommended_Action": action,
            "Resolution_Status": "Pending"
        })

    for _, row in df.iterrows():

        # Check missing values
        for column in MANDATORY_COLUMNS:
            if pd.isna(row[column]):
                add_issue(
                    row, column, "Missing value",
                    "High", "Investigate missing information"
                )

        # Check quantities
        quantity = pd.to_numeric(
            row["Quantity"], errors="coerce"
        )

        if pd.isna(quantity) or quantity % 1 != 0:
            add_issue(
                row, "Quantity", "Invalid quantity type",
                "High", "Review quantity"
            )

        elif quantity < 0:
            add_issue(
                row, "Quantity", "Negative quantity",
                "High", "Investigate possible return"
            )

        elif quantity == 0:
            add_issue(
                row, "Quantity", "Zero quantity",
                "Medium", "Review transaction"
            )

        # Check prices and costs
        for column in ["Unit_Price", "Unit_Cost"]:
            value = pd.to_numeric(
                row[column], errors="coerce"
            )

            if pd.notna(row[column]) and (
                pd.isna(value) or value <= 0
            ):
                add_issue(
                    row, column, "Invalid financial value",
                    "High", "Verify financial information"
                )

        # Check product names
        product = str(row["Product"]).strip().title()

        if row["Product"] != product:
            add_issue(
                row, "Product", "Inconsistent product name",
                "Low", "Standardise product name"
            )

        # Check product-category relationships
        expected_category = PRODUCT_CATEGORIES.get(product)

        if expected_category != row["Category"]:
            add_issue(
                row, "Category", "Invalid product-category relationship",
                "High", "Verify product category"
            )

        # Check dates
        parsed_date = parse_date(row["Date"])

        if pd.isna(parsed_date):
            add_issue(
                row, "Date", "Invalid date",
                "High", "Review transaction date"
            )

        elif str(row["Date"]) != parsed_date.strftime("%Y-%m-%d"):
            add_issue(
                row, "Date", "Inconsistent date format",
                "Low", "Convert to ISO date format"
            )

        # Check discounts
        discount = pd.to_numeric(
            row["Discount_Percent"], errors="coerce"
        )

        if pd.isna(discount) or not 0 <= discount <= 100:
            add_issue(
                row, "Discount_Percent", "Invalid discount",
                "High", "Verify discount percentage"
            )

    # Check duplicate transaction identifiers
    duplicates = df[
        df["Transaction_ID"].duplicated(keep=False)
    ]

    for _, row in duplicates.iterrows():
        add_issue(
            row, "Transaction_ID", "Duplicate transaction ID",
            "High", "Investigate duplicate transaction"
        )

    # Check completely duplicated records
    for _, row in df[df.duplicated(keep=False)].iterrows():
        add_issue(
            row, "Transaction_ID", "Completely duplicated record",
            "High", "Review duplicate record"
        )

    return pd.DataFrame(issues, columns=[
        "Transaction_ID",
        "Affected_Column",
        "Original_Value",
        "Issue_Description",
        "Severity",
        "Recommended_Action",
        "Resolution_Status"
    ])