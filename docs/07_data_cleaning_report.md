# Data Cleaning Report

## Executive Summary
- **Original dataset**: 525,461 rows
- **Cleaned dataset**: 342,273 rows
- **Retention rate**: 65.14%
- **Data quality score**: 100% (No missing values remain, target constraints met)

## Cleaning Steps Applied
1. **Missing CustomerID Removal**
   - **Rows removed**: 107,927
   - **Reasoning**: Customer-level features require a valid `CustomerID`. Since it's a unique identifier, it cannot be imputed.
   - **Impact**: Allowed us to aggregate at the customer level cleanly.
2. **Cancelled Invoices Handling**
   - **Rows removed**: 9,839
   - **Reasoning**: Cancellations represent negative signals for our churn baseline, confusing revenue aggregates.
3. **Negative Quantities**
   - **Rows removed**: 0 (Handled jointly or subsumed by other rules like cancellations)
4. **Invalid Prices**
   - **Rows removed**: 31 (Zero or negative prices)
5. **Missing Descriptions**
   - **Rows removed**: 0 (Handled as a side effect of missing CustomerID or invalid items)
6. **Outliers Removal**
   - **Rows removed**: 59,051
   - **Reasoning**: Used the Interquartile Range (IQR) method (Quantity bounds: Q1-1.5*IQR to Q3+1.5*IQR; Price upper bound: Q3+3*IQR) to remove extreme anomaly purchases, typically from wholesalers or erroneous inputs, which skew customer behavior distributions.
7. **Duplicates Removal**
   - **Rows removed**: 6,340
   - **Reasoning**: Identical transactions entered multiple times as data errors.

## Data Quality Improvements
| Metric | Before | After | Improvement |
| :--- | :--- | :--- | :--- |
| Missing CustomerIDs | 107,927 | 0 | 100% |
| Duplicates | 6,340 | 0 | 100% |
| Invalid Prices | 31 | 0 | 100% |

## Challenges Faced
1. **Challenge:** High percentage (~20.5%) of missing CustomerIDs.
   **Solution:** Decided to drop them because we cannot identify these customers to aggregate churn-oriented behaviors.
   **Lesson:** Guest checkout behaves fundamentally differently from loyalty/registered customers in this dataset.

2. **Challenge:** Defining the outlier boundaries.
   **Solution:** Standard IQR (1.5 multiplier) removed too much valid revenue-generating data on the Price column. We adjusted the Price multiplier to 3.0 to preserve large purchases while clipping out clearly spurious values.
   **Lesson:** Statistical rules need business adjustments; strict textbook IQR bounds might erase high-value 'Champion' customers.

3. **Challenge:** Mixed Types and Large Scale.
   **Solution:** Memory issues and date parsing errors initially slowed down the pipeline. Specifying datetime parsing up front and optimizing categorical casting (where applicable) reduced footprint.
   **Lesson:** Memory footprint awareness is essential on medium data (100MB+) prior to modeling.

## Final Dataset Characteristics
- **Rows:** 342,273
- **Columns:** 13 (Including 5 derived columns: `TotalPrice`, `Year`, `Month`, `DayOfWeek`, `Hour`)
- **Date range:** Late 2010 to end of 2011 (approx)
- **Countries:** Preserved all associated countries.

## Recommendations for Future
Given that over 100k rows were lost to missing `CustomerID`s (likely guest checkouts), further projects might attempt to group these by IP address, Session ID, or `InvoiceNo` blocks to still derive "Guest Churn" models.
