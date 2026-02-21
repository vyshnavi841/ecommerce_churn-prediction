import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
import sys

# Add parent directory to path to import local modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from app.predict import ChurnPredictor
except ImportError:
    st.error("Could not import ChurnPredictor. Ensure you are running from the project root.")

st.set_page_config(
    page_title="E-Commerce Churn Predictor",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_predictor():
    return ChurnPredictor()

def show_home():
    st.title("📊 E-Commerce Customer Churn Prediction")
    st.markdown("This application predicts whether an e-commerce customer is likely to churn within the next 90 days.")
    
    st.markdown("---")
    
    st.markdown("### 🛠️ Model Details")
    st.markdown("**Model Used:** XGBoost Classifier (Champion Model)")
    st.markdown("**Evaluation:** ROC-AUC >= 0.85 with 5-Fold Stratified CV")
    
    st.markdown("### ⚙️ Features")
    st.markdown("**RFM + Behavioral + Temporal Features**")
    st.markdown("- **Recency:** Days since the customer's last purchase.")
    st.markdown("- **Frequency:** Total number of distinct transactions.")
    st.markdown("- **Monetary:** Total lifetime spend & Average Order Value.")
    st.markdown("- **Behavioral:** Purchase velocity, product diversity, and returns.")
    
    st.markdown("### 🚀 Deployment")
    st.markdown("**Platform:** Streamlit containerized in Docker")
    
    st.markdown("---")
    st.info("👈 **Use the sidebar to navigate through the application:** Try single predictions, upload a CSV for batch processing, or view the model dashboard!")

def show_single_prediction(predictor):
    st.title("🔍 Single Customer Prediction")
    st.markdown("Enter customer feature values below:")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        with st.form("customer_input_form"):
            recency = st.slider("Recency (Days since last purchase)", 0, 365, 45)
            frequency = st.number_input("Frequency (Total Invoices)", 1, 100, 5)
            monetary = st.number_input("Total Spent (£)", 0.0, 10000.0, 500.0)
            purchases_30d = st.slider("Purchases in Last 30 Days", 0, 20, 1)
            lifetime_days = st.slider("Customer Lifetime (Days)", 1, 500, 180)
            avg_days_between = st.slider("Avg Days Between Purchases", 0, 100, 30)
            unique_products = st.number_input("Unique Products Bought", 1, 500, 20)
            avg_order_val = monetary / frequency if frequency > 0 else 0
            submit_button = st.form_submit_button("Predict Churn Risk")

    with col2:
        if submit_button:
            customer_data = {
                'Recency': recency, 'Frequency': frequency, 'TotalSpent': monetary,
                'AvgOrderValue': avg_order_val, 'UniqueProducts': unique_products,
                'TotalItems': frequency * 3, 'AvgDaysBetweenPurchases': avg_days_between,
                'Purchases_Last30Days': purchases_30d, 'CustomerLifetimeDays': lifetime_days
            }
            with st.spinner("Analyzing..."):
                result = predictor.predict(customer_data)
                
            prob = result['churn_probability']
            risk = result['risk_level']
            
            fig = go.Figure(go.Indicator(
                mode = "gauge+number", value = prob * 100,
                domain = {'x': [0, 1], 'y': [0, 1]}, title = {'text': "Churn Probability (%)"},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkblue"},
                    'steps' : [
                        {'range': [0, 40], 'color': "lightgreen"},
                        {'range': [40, 75], 'color': "gold"},
                        {'range': [75, 100], 'color': "salmon"}],
                    'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 90}
                }
            ))
            st.plotly_chart(fig, use_container_width=True)
            
            if risk == "High":
                st.error("🚨 HIGH RISK")
            elif risk == "Medium":
                st.warning("⚠️ MEDIUM RISK")
            else:
                st.success("✅ LOW RISK")

def show_batch_prediction(predictor):
    st.title("📤 Batch Prediction")
    st.markdown("Upload a CSV file containing customer data to generate bulk predictions.")
    
    uploaded_file = st.file_uploader("Upload CSV file for batch prediction", type=['csv'])
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.write("Data Preview:")
            st.dataframe(df.head())
            
            if st.button("Predict Batch"):
                with st.spinner("Running predictions..."):
                    predictions = []
                    probabilities = []
                    for _, row in df.iterrows():
                        res = predictor.predict(row.to_dict())
                        predictions.append(res['churn_prediction'])
                        probabilities.append(res['churn_probability'])
                        
                    results_df = df.copy()
                    results_df['Churn_Prediction'] = predictions
                    results_df['Churn_Probability'] = probabilities
                    
                st.success("Batch Prediction Complete!")
                st.dataframe(results_df)
                
                # Provide download link
                csv = results_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download Results as CSV",
                    data=csv,
                    file_name='churn_predictions_batch.csv',
                    mime='text/csv',
                )
        except Exception as e:
            st.error(f"Error processing file: {e}. Ensure columns match the required training schema.")

def show_dashboard():
    st.title("📈 Model Dashboard")
    st.markdown("Overview of the training dataset properties and historical churn.")
    
    col1, col2 = st.columns(2)
    col1.metric("Total Customers", "4,339")
    col2.metric("Historical Churn Rate", "36.6%")
    
    # Sample visualization
    st.subheader("Churn Distribution Chart")
    chart_data = pd.DataFrame(
        {"Status": ["Active", "Churned"], "Count": [2751, 1588]}
    )
    fig = px.bar(chart_data, x="Status", y="Count", color="Status", 
                 color_discrete_map={"Active": "#2ecc71", "Churned": "#e74c3c"})
    st.plotly_chart(fig, use_container_width=True)

def show_documentation():
    st.title("📚 Documentation")
    st.markdown("""
    ### System Architecture
    This application utilizes an XGBoost machine learning model trained on extracting RFM (Recency, Frequency, Monetary) and behavioral data from historical transactions to flag customers who have a high probability of churning in the next 90 days.
    
    ### Tech Stack
    * Frontend: Streamlit
    * Model: XGBoost 2.0.1
    * Containerization: Docker (running Python 3.9)
    
    ### Requirements & Usage
    For Batch Prediction mode, ensure your uploaded CSV contains the exact headers matching the training data feature schema. The raw inference API (`predict.py`) expects a dictionary input scaled identically to the training pipeline.
    """)

def main():
    try:
        predictor = load_predictor()
    except Exception as e:
        st.error(f"Error loading model: {e}")
        st.stop()

    st.sidebar.title("Navigation")
    st.sidebar.markdown("Go to")
    page = st.sidebar.radio("", ["Home", "Single Prediction", "Batch Prediction", "Dashboard", "Documentation"])
    
    if page == "Home":
        show_home()
    elif page == "Single Prediction":
        show_single_prediction(predictor)
    elif page == "Batch Prediction":
        show_batch_prediction(predictor)
    elif page == "Dashboard":
        show_dashboard()
    elif page == "Documentation":
        show_documentation()

if __name__ == "__main__":
    main()
