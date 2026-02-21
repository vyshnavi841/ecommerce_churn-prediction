# E-Commerce Churn Prediction System

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ecommercechurnprediction-cqhr6paivumikvmfa9bezv.streamlit.app/)

## Project Overview
This repository contains an end-to-end Machine Learning pipeline and interactive web application designed to predict customer churn for an e-commerce business using the UCI Online Retail dataset.

By leveraging Recency, Frequency, Monetary (RFM) analysis alongside behavioral and temporal features, this system identifies high-risk customers, allowing the business to proactively intervene and potentially save up to £300,000+ annually in lost revenue.

## Key Features
- **Data Pipeline:** Automated acquisition, cleaning, and preprocessing (handling missing IDs, cancellations, and outliers).
- **Feature Engineering:** Advanced RFM modeling, temporal purchase velocity, and behavioral profiling.
- **Machine Learning:** Tuned XGBoost classifier achieving 0.87 ROC-AUC and 70% recall on the churned class.
- **Interactive UI:** Streamlit web application providing real-time risk scoring, gauge charts, and interpretability for business stakeholders.
- **Deployment Ready:** Fully containerized using Docker and Docker Compose.

## Repository Structure
```
ecommerce-churn-prediction/
│
├── app/                      # Streamlit application & inference scripts
│   ├── predict.py            # Model inference class
│   └── streamlit_app.py      # Streamlit UI
│
├── data/
│   ├── raw/                  # Original downloaded data and metrics
│   └── processed/            # Cleaned data, feature sets, and splits
│
├── deployment/               # Cloud and local deployment guides
│   └── deployment_guide.md
│
├── docs/                     # Comprehensive Phase 1-10 documentation
│   ├── 01_business_problem.md
│   ├── ...
│   └── 14_self_assessment.md
│
├── models/                   # Serialized models, scalers, and metric JSONs
│
├── notebooks/                # Jupyter Notebooks (EDA, Training, Eval)
│
├── src/                      # Core python ETL and Feature scripts
│   ├── 01_data_acquisition.py
│   ├── 02_data_cleaning.py
│   ├── 03_feature_engineering.py
│   └── 04_model_preparation.py
│
├── visualizations/           # Auto-generated plots (EDA, Model Eval)
│
├── Dockerfile                # Image definition
├── docker-compose.yml        # Multi-container orchestration
└── requirements.txt          # Python dependencies
```

## Quick Start (Docker)
The easiest way to run the prediction app is via Docker:
```bash
docker-compose up --build -d
```
Access the application at `http://localhost:8501`.

## Local Setup (Python)
1. Clone the repo and navigate to the root directory.
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `source venv/bin/activate` *(Windows: `venv\\Scripts\\activate`)*
4. Install requirements: `pip install -r requirements.txt`
5. Run the web app: `streamlit run app/streamlit_app.py`

## Running the Complete Pipeline
To regenerate the data, models, and visualizations from scratch, execute the scripts in the `src/` directory sequentially:
```bash
python src/01_data_acquisition.py
python src/02_data_cleaning.py
python src/03_feature_engineering.py
python src/04_model_preparation.py
```
*(Notebooks can be re-run manually or via `jupyter nbconvert --execute` to regenerate evaluation metrics).*

## Model Performance
Our XGBoost model effectively balances precision and recall:
- **ROC-AUC:** 0.87
- **F1-Score:** 0.75
- **Recall:** 0.70 (Captures 7 out of 10 churning customers)
- **Precision:** 0.82 (Low false positive rate for intervention waste)

For a deep dive into the business impact and cost-benefit analysis, see `docs/12_business_impact_analysis.md`.