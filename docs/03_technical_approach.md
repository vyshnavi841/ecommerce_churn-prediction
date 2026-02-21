# Technical Approach

## 1. Classification vs. Regression
We are framing customer churn prediction as a binary classification problem rather than a regression problem. Our goal is to predict a discrete outcome (Will the customer churn? Yes=1, No=0) based on a defined 90-day observation window. A classification approach directly aligns with the business need for actionable probabilities and clear segments of at-risk customers, whereas regression would predict continuous variables (like days until next purchase), which is harder to map strictly to standard business interventions.

## 2. Feature Engineering Needs
Because our raw data is transactional (each row is a purchase), we must aggregate it to the customer level.
- **RFM Features**: Recency (days since last purchase), Frequency (number of purchases), and Monetary (total spend) are proven behavioral descriptors.
- **Behavioral Patterns**: Basket size, average days between purchases, and return rates.
- **Temporal Features**: Customer lifetime, purchase velocity, and recent activity windows (30/60/90 days).

## 3. Multi-Algorithm Testing
No single machine learning algorithm is universally superior. We will test multiple models to find the best balance of performance and interpretability:
- **Logistic Regression**: Serves as our interpretable baseline.
- **Decision Trees & Random Forest**: Handle non-linear relationships well and provide feature importance.
- **Gradient Boosting (e.g., XGBoost)**: Often yields the state-of-the-art performance for tabular data.
- **Neural Networks**: Can potentially capture complex interactions but at the cost of interpretability.

## 4. Deployment Strategy Overview
The final selected model will be serialized along with its preprocessing pipelines (e.g., scalers) using `joblib`. We will build an interactive web application using **Streamlit** that allows users to perform both single-customer predictions manually and batch predictions via CSV upload. This app will be containerized via Docker for reproducibility and finally deployed on Streamlit Community Cloud for public access.
