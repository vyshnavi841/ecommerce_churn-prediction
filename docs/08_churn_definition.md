# Churn Definition

## Problem Statement
We need to define when a customer has "churned" in the context of an e-commerce platform.

## Approach: Observation Window Method
We use an observation window method because customers do not explicitly "cancel" a subscription in retail. Instead, churn is determined by a period of inactivity.

### Step 1: Define Time Windows
Due to variations in dataset extracts, we dynamically calculate the windows based on the latest transaction available in the data:

1. **Find the maximum date**: Let `max_date` be the latest `InvoiceDate`.
2. **Set Observation End**: `observation_end = max_date`.
3. **Set Training Cutoff**: `training_cutoff = max_date - 90 days` (3 months).

- **Training Period**: From the first available date up to `training_cutoff`. Use this data to calculate features.
- **Observation Period**: From `training_cutoff` to `observation_end` (the next 3 months). Use this to determine churn label.

### Step 2: Churn Definition
- **A customer is CHURNED** (1) if: They made at least 1 purchase in the training period, AND they made ZERO purchases in the observation period.
- **A customer is ACTIVE** (0) if: They made at least 1 purchase in the training period, AND they made at least 1 purchase in the observation period.

### Step 3: Implementation Logic
```python
max_date = df['InvoiceDate'].max()
training_cutoff = max_date - pd.Timedelta(days=90)
observation_end = max_date

# Customers who purchased in training period
training_customers = set(df[df['InvoiceDate'] <= training_cutoff]['CustomerID'].unique())

# Customers who purchased in observation period
observation_customers = set(df[(df['InvoiceDate'] > training_cutoff) & 
                               (df['InvoiceDate'] <= observation_end)]['CustomerID'].unique())

# Churn = in training but NOT in observation
# Implemented as checking if CustomerID is NOT in observation_customers
```

## Justification
Why 3 months?
- **Industry Standard**: 90 days represents a typical quarter and is heavily utilized in standard RFM e-commerce segments.
- **Balance**: Balances between too short (marking seasonal buyers as churned too early) and too long (having too few positive churn examples for model training).

## Validation Criteria
- Expected churn rate between 20-40%.
- Strict temporal split: No features in the X matrix can be calculated using data after `training_cutoff`. This absolutely prevents data leakage.
