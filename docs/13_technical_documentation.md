# Technical Documentation

## 1. System Architecture
The system follows a standard modular batch-prediction Pipeline Architecture alongside a real-time inference web app.

### Components:
1. **Data Ingestion (`src/01_data_acquisition.py`)**: Fetches data from UCI repository to `data/raw/`.
2. **Data Processing (`src/02...` & `src/03...`)**: Cleans anomalies, infers missing values where possible, constructs the RFM/Temporal feature matrix, and saves to `data/processed/`.
3. **Model Pipeline (`src/04...` & `notebooks`)**: Handles Train/Val/Test splits (70/15/15), StandardScaling, and XGBoost training. Serializes objects using `joblib`.
4. **Inference API (`app/predict.py`)**: A Python class (`ChurnPredictor`) that loads the serialized model and scaler, preprocesses a single JSON/dictionary input exactly as trained, and outputs predictions.
5. **Presentation Layer (`app/streamlit_app.py`)**: A Streamlit dashboard consuming the `ChurnPredictor` to provide an interactive GUI.

## 2. Feature Engineering Pipeline details
- **Target Variable Generation:** 
  - Dynamic observation window calculation.
  - Cutoff = `max_date - 90 days`.
  - Label = 1 if customer exists before cutoff but has 0 purchases after cutoff.
- **Handling Data Leakage:**
  - Strict temporal splits were enforced. The feature data (`X`) only aggregates transactions occurring *before* the cutoff date.
- **Imputation:**
  - After calculating features, missing numeric values (e.g., standard deviation of a single-item basket) were imputed with the median. Categorical modes were used for missing strings.

## 3. Modeling Methodology
- **Algorithm:** XGBoost
- **Hyperparameters:**
  - `n_estimators`: 200 (sufficient to converge without overfitting).
  - `max_depth`: 5 (shallow enough to prevent leaf-memorization).
  - `learning_rate`: 0.05 (slower learning for better generalization).
  - `scale_pos_weight`: Automatically calculated based on `(Total Active) / (Total Churned)` to penalize false negatives more heavily during gradient updates.

## 4. Dependencies & Environments
The project uses `pandas`, `scikit-learn`, `xgboost`, `streamlit`, and `plotly`. 
Environment consistency is guaranteed via `Dockerfile` which isolates the Python 3.9 runtime.

## 5. Known Limitations
- **Cold Start:** The model requires a customer to have made at least one purchase before the 90-day window to calculate RFM features. Brand new customers have zero historical features and cannot be scored accurately.
- **Missing Customer IDs:** ~25% of the raw transactions are missing Customer IDs (likely guest checkouts). This model only scores registered/identifiable customers. Future work should attempt session-based fingerprinting for guest users.
