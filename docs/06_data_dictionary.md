# Data Dictionary

## Raw Dataset: `online_retail.csv`

| Column Name | Data Type | Description | Example Values | Missing % | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **InvoiceNo** | String | 6-digit invoice number, 'C' prefix = cancellation | 536365, C536365 | 0% | Unique identifier for a transaction. |
| **StockCode** | String | 5-digit product code | 85123A, 22423 | 0% | Some non-standard codes exist (e.g. POST). |
| **Description** | String | Product name | WHITE HANGING HEART T-LIGHT HOLDER | ~0.27% | Clean required (some are manual entries or errors). |
| **Quantity** | Integer | Quantity per transaction | 6, -1 | 0% | Negative signifies a returned item or cancellation. |
| **InvoiceDate** | DateTime | Transaction timestamp | 2010-12-01 08:26:00 | 0% | Range covers approximately late 2010 to end of 2011. |
| **UnitPrice** | Float | Price per unit in GBP (£) | 2.55, 0.00 | 0% | Some zeros exist which need cleaning. |
| **CustomerID** | Float | 5-digit customer identifier | 17850.0, 12346.0 | ~24.9% | High missing rate; needs dropping. |
| **Country** | String | Customer country | United Kingdom, France | 0% | Over 35 unique countries represented. |

## Data Quality Issues Identified
1. **Missing Customer IDs**: Roughly 25% of the data does not have a linked customer record, meaning these transactions cannot be used for customer profiling.
2. **Missing Descriptions**: A very small subset of rows has missing product descriptions.
3. **Cancelled Invoices**: Certain invoices begin with 'C', representing cancellations, and inherently have negative numerical quantities.
4. **Invalid Unit Prices**: Some transactions are logged with a UnitPrice of 0 or less.
5. **Extreme Outliers**: Large anomalous purchases (e.g. Quantity = 80995) or exceedingly high prices distort averages.
6. **Data Types**: `InvoiceDate` is currently parsed as a string to start with, requiring datetime casting. `CustomerID` needs to be integer-casted.

## Data Cleaning Required
1. Remove transactions missing `CustomerID`.
2. Remove any invoice number starting with 'C' (Cancellations).
3. Remove records with `Quantity <= 0`.
4. Remove records with `UnitPrice <= 0`.
5. Remove rows without a `Description`.
6. Calculate IQR for `Quantity` and `UnitPrice` and remove extreme outliers.
7. Drop aggregate duplicate rows.
8. Create derived chronological columns (`Year`, `Month`, `DayOfWeek`, `Hour`) and `TotalPrice` (`Quantity * UnitPrice`).
9. Properly cast column data types (`CustomerID` to int, categorical columns to category).
