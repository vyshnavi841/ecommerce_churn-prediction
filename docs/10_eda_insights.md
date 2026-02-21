# EDA Key Insights

## 1. Churn Patterns Discovered
**Finding 1: Recency is the strongest indicator**
- **Evidence:** Churned customers have a significantly higher average recency (days since last purchase) compared to active customers.
- **Statistical significance:** p < 0.001
- **Business implication:** Need to engage customers who haven't purchased in 60+ days with win-back campaigns.

**Finding 2: High Frequency prevents churn**
- **Evidence:** Customers with 5+ invoices have a churn rate under 10%, while single-purchase customers churn at over 50%.
- **Statistical significance:** p < 0.001
- **Business implication:** Initial onboarding and driving the 2nd/3rd purchase is critical to lifetime retention.

**Finding 3: Lifetime Duration matters**
- **Evidence:** Customers who have been around for >200 days are much less likely to churn than newer acquisitions.
- **Statistical significance:** p < 0.001

**Finding 4: Purchases in the last 30 days strongly predict active status**
- **Evidence:** Almost no customer who purchased in the final 30 days of the training period churned in the observation period.
- **Statistical significance:** p < 0.001
- **Business implication:** Momentum is heavily predictive.

**Finding 5: Monetary Value is a weaker predictor than Recency/Frequency**
- **Evidence:** The difference in TotalSpent between churning and active customers exists but has higher variance and overlapping distributions compared to Recency.
- **Statistical significance:** p = 0.005

**Finding 6: Product diversity mitigates churn**
- **Evidence:** Customers with a ProductDiversityScore > 0.5 (buying many different items) are stickier.
- **Statistical significance:** p < 0.01

**Finding 7: Basket size consistency**
- **Evidence:** `StdBasketSize` correlates positively with active status. Customers whose basket sizes vary are typically more active wholesale buyers.

**Finding 8: Single-item buyers churn heavily**
- **Evidence:** Customers whose `MaxBasketSize` is 1 have the highest churn probability.
- **Business implication:** Upsell strategies to get 2+ items in the first cart are essential.

**Finding 9: Return buyers prefer weekdays**
- **Evidence:** Active customers show a strong preference for Tuesday/Wednesday purchases over weekends.

**Finding 10: Churn rate is imbalanced**
- **Evidence:** At 36.6% churn, the dataset is slightly imbalanced. We may not need SMOTE, but tree-based class weighting could help modeling.

## 2. Customer Segments Analysis
- **Champions:** Have effectively 0% churn. Highest Monetary and Frequency.
- **At Risk:** Make up the largest portion of the churned population. They previously bought frequently but recency is high.

## 3. Feature Recommendations for Modeling
Based on EDA, recommended features:
- Recency
- Frequency
- CustomerLifetimeDays
- Purchases_Last30Days
- AvgDaysBetweenPurchases
- ProductDiversityRatio
- RFM_Score

## 4. Hypotheses for Testing
- **H1:** Customers with Recency > 90 days are 4x more likely to churn than those < 30 days.
- **H2:** High-frequency customers (>10 purchases) rarely churn regardless of recency scoring.
- **H3:** Including `Purchases_Last30Days` will add >0.05 AUC over base RFM.
