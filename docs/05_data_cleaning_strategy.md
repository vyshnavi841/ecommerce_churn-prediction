# Data Cleaning Strategy

## 1. Missing Values Strategy
### CustomerID (Missing: ~25%)
**Decision:** DROP
**Reasoning:** Since our goal is customer churn prediction, we must aggregate transactions to the customer level to build a profile. Transactions without a `CustomerID` cannot be assigned to any profile. We cannot use imputation because `CustomerID` is a unique identifier.
**Impact:** We will remove approximately 135,000 rows (depending on exact counts).

### Description (Missing: <1%)
**Decision:** DROP
**Reasoning:** While removing descriptions drops a small percentage of rows, we want to look at product affinity. Transactions without products aren't useful for building product features. Given the very low missing percentage, removal is trivial.

## 2. Handling Cancellations
**Issue:** Invoices starting with 'C' are cancellations.
**Strategy:**
**Option A:** Remove all cancellations (Chosen)
**Reasoning:** Our target is churn prediction based on positive purchasing behavior. Returns complicate feature engineering for "Monetary" (spend) and "Basket Size", as negative quantities skew aggregates. By excluding returns, we cleanly focus on actual successful purchases.

## 3. Negative Quantities
**Issue:** Negative quantities indicate returns or administrative adjustments.
**Strategy:** Filter for `Quantity > 0`. We will completely remove negative quantities for the same reasons as cancellations. We are interested in positive buying signals.

## 4. Outliers
### Quantity Outliers
**Detection Method:** IQR (Interquartile Range)
**Threshold:** Q1 - 1.5 * IQR to Q3 + 1.5 * IQR
**Action:** Remove or Cap. We will remove extreme outliers because wholesale purchases (e.g. 80,000 items) are likely anomalies or B2B transactions which distort standard B2C churn models.

### Price Outliers
**Strategy:** Remove zero/negative prices first. Then apply the IQR method to remove extreme unit prices, which might represent non-product charges like manual adjustments or fees (e.g., POSTAGE can be huge).

## 5. Data Type Conversions
- `InvoiceDate`: Convert to `datetime64[ns]` for temporal features.
- `CustomerID`: Convert to `integer` (after dropping missing values).
- `UnitPrice`: Keep as numeric (`float`).
- `StockCode`, `Country`: Convert to `category` for memory efficiency.

## 6. Duplicate Handling
**Strategy:** We will define duplicates as rows with the same `InvoiceNo`, `StockCode`, `CustomerID`, `InvoiceDate`, `Quantity`, and `UnitPrice`. These will be dropped using `df.drop_duplicates()`, as they likely represent system entry errors rather than identical items scanned twice (since `Quantity` covers multiple items).
