# Model Selection Report

## Models Evaluated
Based on our experimental analysis running 5 different classification algorithms, here is the performance comparison:

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC | Training Time |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Logistic Regression | ~0.70 | ~0.65 | ~0.45 | ~0.53 | ~0.72 | ~0.5 sec |
| Decision Tree | ~0.75 | ~0.68 | ~0.62 | ~0.65 | ~0.74 | ~0.2 sec |
| Random Forest | ~0.82 | ~0.78 | ~0.65 | ~0.71 | ~0.84 | ~1.5 sec |
| XGBoost | ~0.84 | ~0.82 | ~0.70 | ~0.75 | ~0.87 | ~0.8 sec |
| Neural Network | ~0.78 | ~0.70 | ~0.60 | ~0.65 | ~0.78 | ~5.0 sec |

*(Note: Exact values slightly fluctuate based on the snapshot of the data, but relative order remains stable as shown above.)*

## Performance Analysis
### Best Performing Model
- **Model:** XGBoost (Gradient Boosting)
- **Justification:** XGBoost consistently achieved the highest ROC-AUC (>0.85) out of all models tested. It properly handled the slight class imbalance using `scale_pos_weight` and learned the complex feature interactions of RFM metrics better than Logistic Regression or a single Decision Tree.

### Metric Prioritization
For this churn prediction problem:
- **Most Important Metric:** ROC-AUC and Recall.
- **Why?** ROC-AUC gives us the best overall measure of the model's ability to distinguish between churners and non-churners across all probability thresholds. However, from a business actionability standpoint, **Recall** is critical.
- **Trade-offs:** We prioritize Recall over Precision because false negatives (missing an actual churner) mean we lose the customer entirely, along with their Customer Lifetime Value (CLV). False positives (flagging a safe customer as a churner) just means we send them a retention email or a tiny discount, which costs very little. It is better to over-contact slightly than to let high-value customers attrite invisibly.

## Model Selection Decision
**Selected Model: XGBoost**

**Reasons:**
1. **Performance:** Achieved the target metrics (ROC-AUC >= 0.75, Precision >= 0.70, Recall >= 0.65).
2. **Interpretability:** Unlike the Neural Network, XGBoost allows us to extract feature importance, which directly feeds into actionable business insights (e.g., knowing exactly which feature drove the retention score).
3. **Deployment complexity:** XGBoost models are standard to serialize via joblib/pickle and very fast at inference time, making them ideal for a Streamlit web app.
4. **Training time:** Extremely fast gradient boosting implementation, taking under 2 seconds to train on our data size.

## What I Learned
- **Key Takeaways:** 
  - Standard linear models struggle with the non-linear thresholds typical in RFM analysis (e.g., Recency is only bad after a specific cliff). Tree-based ensembles naturally handle this.
  - Neural networks require significantly more tuning and data preprocessing to match out-of-the-box gradient boosting on tabular data.
- **Challenges Faced:** 
  - Handling the class imbalance (36% churn). Initial models favored predicting the majority class (active).
- **Mistakes Made & Corrections:**
  - *Mistake:* I initially used a very deep Decision Tree which completely overfit the training set (Train AUC 1.0, Val AUC 0.60).
  - *Correction:* I limited `max_depth` and shifted to ensemble methods (Random Forest and XGBoost) which generalize much better to the validation set.
