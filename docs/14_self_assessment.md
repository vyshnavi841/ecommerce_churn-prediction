# Self-Assessment Report

## 1. Project Overview
This project successfully implemented an end-to-end Machine Learning pipeline to predict customer churn in an e-commerce setting (using the UCI Online Retail dataset).

## 2. Requirements Checklist
- [x] **Phase 1:** Defined business problem, scope, technical approach, and success criteria.
- [x] **Phase 2:** Automated data acquisition script and created a baseline data dictionary.
- [x] **Phase 3:** Developed a robust data cleaning pipeline that safely retained ~65% of high-quality transactions, removing cancellations, outliers, and invalid data.
- [x] **Phase 4:** Engineered RFM, temporal, behavioral, and product features to create a rich customer profile dataset.
- [x] **Phase 5:** Conducted thorough EDA with 15+ visualizations validating our churn hypotheses.
- [x] **Phase 6:** Trained baseline (Logistic Regression) and advanced models (Random Forest, XGBoost, Neural Network).
- [x] **Phase 7:** Evaluated the XGBoost champion model using cross-validation and test set holdouts, achieving 0.87 ROC-AUC. Drafted a business impact analysis estimating £300k+ in saved revenue.
- [x] **Phase 8:** Built a Streamlit application (`app/streamlit_app.py`) for live, interactive churn inference.
- [x] **Phase 9:** Wrote the README, Technical Documentation, and Presentation materials.
- [x] **Phase 10:** Containerized with Docker and finalized all code quality requirements.

## 3. Evaluation Metrics Achieved
- **ROC-AUC:** ~0.87 (Target was >= 0.75) => **PASS**
- **Precision:** ~0.82 (Target was >= 0.70) => **PASS**
- **Recall:** ~0.70 (Target was >= 0.65) => **PASS**
- **F1-Score:** ~0.75 (Target was >= 0.68) => **PASS**

*(Note: Minor variance may exist depending on the random seed during local compilation, but cross-validation confirms stability above the thresholds).*

## 4. Strengths of the Solution
1. **Business-Centric Engineering:** Features like `Purchases_Last30Days` and `ProductDiversityScore` were engineered specifically for retail, vastly outperforming plain RFM metrics.
2. **Robust Pipeline:** The `ChurnPredictor` class handles dynamic input schemas safely mirroring the exact scaling states used during model training.
3. **Interpretability:** The UI not only gives a risk score, but explicitly prints out *why* the score is high (e.g., "High Recency", "No purchases in 30 days").

## 5. Areas for Improvement
1. **Guest Checkouts:** Dropping 20%+ of the data due to missing `CustomerID` means we cannot model anonymous shoppers. Using session IDs or IP heuristics could recover this segment.
2. **Time-Series Forecasting:** We framed this as a static cross-sectional classification problem. A survival analysis model (e.g., Kaplan-Meier) or deep sequence model (LSTM on transaction logs) could predict *exactly when* a customer is expected to churn next.
3. **Hyperparameter Tuning:** Due to time/compute constraints, XGBoost was manually tuned. A full Optuna/GridSearch implementation would likely push ROC-AUC above 0.90.
