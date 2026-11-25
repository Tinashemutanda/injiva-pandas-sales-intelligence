# ZimTech Retail Holdings
## Sales Intelligence and Management Report

Prepared by:Tinashe Mutanda  
Organisation:INJIVA Digital Systems  
Reporting period:January 2026  
Currency:USD

## 1. Executive Summary

This project investigated, cleaned and analysed retail sales transactions to support reliable financial reporting and evidence based management decisions.Of the 20 original transactions, 17 were accepted and three were rejected for further investigation, resulting in an acceptance rate of 85%.he accepted transactions generated $13,340.50 in net revenue and $3,255.50 in gross profit, representing an overall gross profit margin of 24.40%.

The analysis recommends prioritising Harare, the Computers category and Mary for controlled future investment.

## 2. Data Quality Findings

The investigation identified:

- Inconsistent product names.
- Inconsistent date formats.
- Missing selling prices.
- Negative transaction quantities.
- Zero transaction quantities.

Three transactions were rejected:

| Transaction | Reason |
|---|---|
| TX009 | Negative quantity |
| TX012 | Missing selling price |
| TX015 | Zero quantity |

TX009 could represent a return with a potential revenue adjustment of negative $400, subject to verification.

TX012 has a recorded quantity of two units and a potential cost of $330, but its revenue and profitability cannot be determined without the missing selling price.

TX015 contributes no revenue under its recorded zero quantity but requires investigation.

The original records were preserved for auditing. No missing financial values were invented.

## 3. Revenue and Profitability Analysis

| Financial indicator | Result |
|---|---:|
| Gross revenue | $14,033.00 |
| Total discounts | $692.50 |
| Net revenue | $13,340.50 |
| Total cost | $10,085.00 |
| Gross profit | $3,255.50 |
| Gross profit margin | 24.40% |
| Average transaction value | $784.74 |
| Valid transactions | 17 |
| Units sold | 111 |

The company generated positive gross profit across all accepted transactions. Gross profit does not represent net profit because operating expenses were not supplied.

## 4. Product Performance

| Product | Net revenue | Gross profit | Margin |
|---|---:|---:|---:|
| Smartphone | $5,831.50 | $1,096.50 | 18.80% |
| Laptop | $3,903.00 | $853.00 | 21.85% |
| Monitor | $1,246.00 | $296.00 | 23.76% |
| Printer | $877.00 | $217.00 | 24.74% |
| Keyboard | $742.00 | $393.00 | 52.96% |
| Mouse | $741.00 | $400.00 | 53.98% |

Smartphones generated the highest product revenue and gross profit. However, their margin was below the overall company margin.

Accessories demonstrated strong profitability relative to revenue, suggesting opportunities for complementary product sales.

### Category Performance

| Category | Revenue | Profit | Margin | Units |
|---|---:|---:|---:|---:|
| Mobile | $5,831.50 | $1,096.50 | 18.80% | 20 |
| Computers | $5,149.00 | $1,149.00 | 22.32% | 13 |
| Accessories | $1,483.00 | $793.00 | 53.47% | 74 |
| Office Equipment | $877.00 | $217.00 | 24.74% | 4 |

Computers generated the highest total gross profit, while Mobile generated the highest revenue.

## 5. City-Level Performance

| City | Revenue | Profit | Margin | Transactions |
|---|---:|---:|---:|---:|
| Harare | $4,239.50 | $992.50 | 23.41% | 5 |
| Mutare | $4,134.00 | $794.00 | 19.21% | 4 |
| Bulawayo | $3,724.00 | $804.00 | 21.59% | 3 |
| Gweru | $1,243.00 | $665.00 | 53.50% | 5 |

Harare generated the highest recorded revenue and gross profit.

Gweru achieved the highest gross profit margin, supported by accessory sales.

No transactions were supplied for Masvingo. This does not establish that the city had no business activity.

## 6. Salesperson Performance

| Salesperson | Revenue | Profit | Margin | Transactions |
|---|---:|---:|---:|---:|
| Mary | $4,239.50 | $992.50 | 23.41% | 5 |
| Sarah | $4,134.00 | $794.00 | 19.21% | 4 |
| John | $3,724.00 | $804.00 | 21.59% | 3 |
| Peter | $1,243.00 | $665.00 | 53.50% | 5 |

Mary generated the highest recorded revenue and gross profit.

Peter achieved the highest profit margin and sold 66 units.

Salesperson comparisons should consider differences in product mix, location and customer demand.

## 7. Business Recommendations

1. **Prioritise Harare:** Conduct a controlled investment pilot because Harare generated $4,239.50 in revenue and $992.50 in gross profit.

2. **Invest in Computers:** Prioritise laptops and monitors because the Computers category generated the highest category gross profit of $1,149.00.

3. **Develop Mary's sales capacity:** Provide additional training and sales support based on her leading revenue and gross profit performance.

4. **Promote accessory cross-selling:** Accessories achieved a 53.47% gross profit margin and accounted for 74 of the 111 units sold. Bundle accessories with computers and smartphones.

5. **Review smartphone discounts and procurement costs:** Mobile generated substantial revenue but achieved a relatively low margin of 18.80%.

6. **Improve transaction validation:** Introduce mandatory price fields, standardised product identifiers, consistent date formats and automated quantity validation.

7. **Investigate rejected transactions:** Resolve TX009, TX012 and TX015 before including them in financial reports.

8. **Improve geographical data coverage:** Obtain additional records from all five cities, particularly Masvingo, before making long term expansion decisions.

## 8. Dataset Limitations and Assumptions

- The dataset contains only 20 fictional transactions.
- Only 17 transactions were accepted for financial reporting.
- The analysis covers January 2026 only.
- Operating expenses, taxes and inventory balances were not supplied.
- Missing dates do not necessarily indicate zero sales.
- Product reference codes and reorder thresholds are illustrative assumptions.
- Revenue-based classifications do not independently measure profitability.
- Salesperson performance is influenced by location and product mix.
- Investment recommendations require confirmation using larger datasets.

## 9. Technical Implementation

The solution was developed using Python, Pandas, NumPy, Jupyter Notebook, pytest, Git and GitHub.

The implementation includes:

- Reusable schema validation.
- Rule-based data quality assessment.
- Deterministic data cleaning.
- Financial transformations.
- Multi-level aggregation.
- Time-series analysis.
- Product and transaction segmentation.
- Validated DataFrame joins.
- Pivot tables and financial reconciliation.
- Automated testing.
- A reusable processing pipeline.
- CSV report generation.

Original records remain available for auditing.

## 10. Reproduction Instructions

Install the required dependencies:

`python -m pip install -r requirements.txt`

Execute the processing pipeline:

`python -m src.pipeline`

Execute automated tests:

`python -m pytest tests/ -v`

Open `notebooks/sales_analysis.ipynb` and run all cells to reproduce the detailed analysis.

Generated reports are stored in the `data/` directory.

## 11. Final Management Challenge

ZimTech Retail Holdings should provisionally prioritise:

| Investment area | Recommendation | Evidence |
|---|---|---|
| City | Harare | Highest city revenue and profit |
| Category | Computers | Highest category gross profit |
| Salesperson | Mary | Highest salesperson revenue and profit |

These recommendations balance revenue, gross profit, transaction volumes and operational considerations.

However, Computers and Harare have margins below the overall company margin. Management should therefore combine investment with margin improvement and accessory cross-selling.

The recommendations should be implemented as controlled pilots rather than immediate large-scale expansion because of the small dataset and unresolved data quality issues.

## Conclusion

The project establishes a reproducible sales intelligence solution that improves data quality, financial accuracy and management reporting. Automated validation, reusable processing functions and version control provide a foundation for future analytical development.