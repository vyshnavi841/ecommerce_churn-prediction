# Customer Churn Prediction: E-Commerce Case Study

## Executive Summary
**Objective:** Identify customers likely to stop buying within 90 days.
**Solution:** A Machine Learning (XGBoost) model analyzing transaction history to flag high-risk customers for targeted retention campaigns.

---

## 1. The Business Problem
Customer acquisition costs are 5x higher than retention costs. By the time a customer "churns", the revenue is already gone. 
- **Goal:** Predict churn *before* it becomes permanent.
- **Definition:** An active customer who will make 0 purchases in the next 90 days.

---

## 2. Approach: RFM & Machine Learning
We moved past simple demographics and utilized behavioral data:
- **Recency:** Days since last order.
- **Frequency:** Total historical orders.
- **Monetary:** Total value of those orders.
- **Temporal/Velocity:** Purchases in the last 30 days (capturing fading momentum).

---

## 3. Key Findings from Data
1. **Recency is King:** Customers passing the 60-day mark without a purchase are highly likely to churn.
2. **The 30-Day cliff:** Any purchase activity in the 30 days prior to the cutoff almost guaranteed retention.
3. **Product Diversity Matters:** Customers who explore the catalog (buying many different items) are much "stickier" than those who buy a single bulk item.

---

## 4. Model Performance
**Selected Model: XGBoost**
- **Accuracy:** 84% - Correctly predicts overall status.
- **Recall:** 70% - Successfully identifies 7 out of 10 true churners.
- **Precision:** 82% - Highly accurate when flagging a risk, minimizing wasted marketing spend on false alarms.

---

## 5. Financial ROI Estimate
For a baseline of 4,000 active customers:
- **At-Risk Revenue:** ~£1.5 Million annually.
- **Targeted Campaign Cost:** ~£37,500 (Focusing only on the 30% flagged by XGBoost).
- **Projected Lift:** Saving just 30% of these identified churners yields **~£300,000+** in retained top-line revenue.

---

## 6. Next Steps
1. Immediate integration with CRM (Salesforce/HubSpot).
2. Launch a pilot VIP Retention program for high-probability, high-monetary-value churners.
3. Establish A/B testing protocols to measure the exact causal impact of these interventions.
