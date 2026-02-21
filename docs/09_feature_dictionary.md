# Feature Dictionary

## Target Variable
| Feature | Type | Description | Example | Business Meaning |
| :--- | :--- | :--- | :--- | :--- |
| **Churn** | Binary | 1=Churned, 0=Active | 1 | Customer didn't purchase in the 3-month observation window. |

## RFM Features
| Feature | Type | Description | Range | Business Meaning |
| :--- | :--- | :--- | :--- | :--- |
| **Recency** | Integer | Days since last purchase | 0-600 | Lower = more recently engaged customer. |
| **Frequency** | Integer | Number of unique invoices/purchases | 1-200+ | Higher = more loyal, habitual buyer. |
| **TotalSpent** | Float | Total money spent (£) | 0-50000+ | Customer lifetime value (Monetary). |
| **AvgOrderValue** | Float | Average spend per invoice | 10-1000 | Indicates whether they make small or large purchases. |
| **UniqueProducts** | Integer | Count of distinct items bought | 1-2000 | Breadth of catalog exploration. |
| **TotalItems** | Integer | Total absolute quantity of items | 1-5000 | High volume buyer indication. |

## Behavioral Features
| Feature | Type | Description | Range | Business Meaning |
| :--- | :--- | :--- | :--- | :--- |
| **AvgDaysBetweenPurchases** | Float | Avg days gaps between invoices | 0-300 | Natural purchase cadence. |
| **AvgBasketSize** | Float | Mean items per basket | 1-500 | Standard trip size. |
| **StdBasketSize** | Float | Std dev of items per basket | 0-100 | Consistency of shopping trips. |
| **MaxBasketSize** | Integer | Max items in a single basket | 1-2000 | Propensity for occasional large hauls. |
| **PreferredDay** | Integer | Mode of purchase day (0-6) | 0-6 | Optimizes email targeting days. |
| **PreferredHour** | Integer | Mode of purchase hour (0-23) | 6-22 | Optimizes intra-day engagement. |
| **CountryDiversity** | Integer | Number of unique countries shipped | 1-3 | Usually 1; anomalies might signify businesses or expats. |

## Temporal Features
| Feature | Type | Description | Range | Business Meaning |
| :--- | :--- | :--- | :--- | :--- |
| **CustomerLifetimeDays** | Integer | Days between first & last purchase | 0-400 | Total tenure of the customer. |
| **PurchaseVelocity** | Float | Frequency / CustomerLifetimeDays | 0-1.0 | Speed of purchases. |
| **Purchases_Last30Days** | Integer | Invoices in last 30 days of training | 0-20 | Recent momentum before cutoff. |
| **Purchases_Last60Days** | Integer | Invoices in last 60 days | 0-30 | Recent momentum before cutoff. |
| **Purchases_Last90Days** | Integer | Invoices in last 90 days | 0-50 | Recent momentum before cutoff. |

## Product Features
| Feature | Type | Description | Range | Business Meaning |
| :--- | :--- | :--- | :--- | :--- |
| **ProductDiversityScore** | Float | Ratio of unique to total products | 0-1.0 | Are they repeatedly buying the same thing (0) or exploring the catalog (1)? |
| **AvgPricePreference** | Float | Mean unit price of items bought | 0-100 | Do they buy cheap or luxury items? |
| **StdPricePreference** | Float | Std dev of unit price | 0-100 | Variation in item prices. |
| **MinPrice** | Float | Minimum price paid | 0-50 | Bottom-tier sensitivity. |
| **MaxPrice** | Float | Maximum price paid for a single item | 5-1000 | Willingness to buy big-ticket items. |
| **AvgQuantityPerOrder** | Float | Average volume per item ordered | 1-500 | Bulk purchaser vs retail purchaser. |

## Segmentation Features
| Feature | Type | Description | Range | Business Meaning |
| :--- | :--- | :--- | :--- | :--- |
| **RecencyScore** | Integer | Quantile rank for recency (1-4) | 1-4 | Standardized bin (4 is best, i.e., lowest days). |
| **FrequencyScore** | Integer | Quantile rank for frequency (1-4) | 1-4 | Standardized bin (4 is best). |
| **MonetaryScore** | Integer | Quantile rank for spend (1-4) | 1-4 | Standardized bin (4 is best). |
| **RFM_Score** | Integer | Sum of the three scores | 3-12 | Aggregate customer health. |
| **CustomerSegment** | String | Heuristic label based on RFM_Score | Categorical | Champions, Loyal, At Risk, Lost, etc. |

## Feature Engineering Decisions
We selected standard RFM techniques extended by Temporal features because standard RFM lacks velocity metrics. By looking at "Purchases in the last 30 days", the model can capture the decaying momentum of a customer better than a simple flat Frequency scalar.

### Feature Interactions
`CustomerLifetimeDays` and `Frequency` interact via `PurchaseVelocity`. Without velocity, a customer who bought 10 times over 2 years looks identical in frequency to one who bought 10 times in 2 months.

### Feature Importance Hypothesis
Based on typical e-commerce behavior:
1. `Recency` will be the strongest negative predictor of activity.
2. `Purchases_Last30Days` / `Purchases_Last60Days` will be the strongest positive predictors preventing churn.
3. `FrequencyScore` will have a non-linear buffering effect (high frequency buys us tolerance on recency).
