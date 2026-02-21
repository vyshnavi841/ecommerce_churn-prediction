# Business Impact Analysis

## Executive Summary
Deploying the XGBoost Churn Prediction Model is projected to save the company **£180,000 to £350,000 annually** by enabling proactive retention of high-value customers. 

## Model Performance Context
The final selected model achieved:
- **ROC-AUC:** ~0.87
- **Precision:** ~0.82
- **Recall:** ~0.70
- **Accuracy:** ~0.84

**What this means:**
When the model flags a customer as "At Risk of Churning", it is correct 82% of the time (Precision). Furthermore, it successfully identifies 70% of all customers who will actually churn (Recall). 

## Cost-Benefit Analysis

### Assumptions based on Validation Data
- Average Order Value (AOV): ~£260
- Average Yearly Spend per Active Customer: ~£1,080
- Customer Base: ~4,000
- Baseline Churn Rate: 36.6% 
- Total Customers Churning per Year: ~1,464 
- Total Revenue At Risk: ~£1.58 Million

### Scenario 1: No Intervention (Status Quo)
- Expected Revenue Loss: **£1,580,000**
- Retention Costs: £0
- Net Loss: **£1,580,000**

### Scenario 2: Blanket Retention Campaign (Targeting Everyone)
Assume we offer a £20 voucher to all 4,000 customers to prevent churn.
- Campaign Cost: £80,000
- False Positive Waste: Sending discounts to the 63.4% of customers who would have stayed anyway (Cost = £50,720 wasted).
- *This is highly inefficient and trains active customers to wait for discounts.*

### Scenario 3: AI-Driven Targeted Retention (Using XGBoost)
We only target the customers flagged by the model as "At Risk".
- **Total Flagged for Retention:** ~1,250 
- **True Positives (Will Churn):** 1,024 (70% recall of the 1,464 total churners)
- **False Positives (Will Stay):** 226 (calculated from 82% precision)

**Intervention Economics:**
Let's assume a proactive phone call + personalized £30 discount voucher has a 30% success rate in retaining a churning customer.
- **Cost of Campaign:** 1,250 targeted * £30 = **£37,500**
- **Revenue Saved:** 1,024 true churners identified * 30% success rate * £1,080 avg lifetime spend = **£331,776**
- **Net Financial Impact:** £331,776 (Saved) - £37,500 (Cost) = **£294,276 Profit**

## Next Steps for the Business
1. **Integration:** Connect the model's output (probability scores) to the CRM system (e.g., Salesforce or HubSpot).
2. **Tiered Interventions:**
   - **High Probability Churn (>80%) + High Monetary Value:** Trigger VIP customer success call.
   - **Medium Probability (60-80%) + Low Monetary:** Send automated 15% discount email.
   - **Low Probability (<40%):** Do nothing (save margin).
3. **A/B Testing:** Hold out 10% of the "At Risk" segment as a control group to perfectly measure the uplift of the campaign over a 3-month period.
