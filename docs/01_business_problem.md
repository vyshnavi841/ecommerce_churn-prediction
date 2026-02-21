# Business Problem Statement

## 1. Business Context
The e-commerce industry is highly competitive, and acquiring new customers has become increasingly challenging and expensive. In fact, acquiring a new customer can cost anywhere from 5 to 25 times more than retaining an existing one. Furthermore, a 5% increase in customer retention can lead to an increase in profits of 25% to 95%.

Currently, "RetailCo Analytics" faces significant pain points regarding customer retention. A large volume of customers make initial purchases but fail to return, resulting in a low repeat purchase rate. The marketing and sales teams currently lack the analytical insights needed to proactively identify customers at risk of leaving before they actually churn, leading to generic and often ineffective marketing campaigns.

## 2. Problem Definition
The overarching problem is to predict whether a customer will churn. 
**Definition of Churn**: "A customer who hasn't made a purchase in the last 90 days."

## 3. Stakeholders
- **Marketing Team**: Needs customer segments to run targeted and personalized retention campaigns.
- **Sales Team**: Needs prioritized churn predictions to offer timely discounts and incentives.
- **Product Team**: Needs product insights (e.g., product affinity) to understand which products drive loyalty.
- **Executive Team**: Needs ROI projections to justify the budget for retention campaigns and data infrastructure.

## 4. Business Impact
Implementing an accurate churn prediction system will have the following expected impact:
- **Expected reduction in churn rate**: Target 15-20% reduction through proactive interventions.
- **Projected revenue increase**: By retaining high-value customers who spend consistently.
- **Cost savings**: Reduced marketing spend by targeting only at-risk customers instead of a blanketing approach.

## 5. Success Metrics
To deem this predictive solution a success, the model must achieve the following technical targets:
- **Primary Metric**: ROC-AUC Score > 0.78
- **Secondary Metrics**:
  - Precision > 0.75 (minimize false positives so we don't waste budget on non-churners)
  - Recall > 0.70 (maximize the capture of actual churners)
  - F1-Score > 0.72
