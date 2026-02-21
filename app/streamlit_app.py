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
    from predict import ChurnPredictor

st.set_page_config(
    page_title="E-Commerce Churn Predictor",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
    .churn-high { color: #e74c3c; font-weight: bold; }
    .churn-medium { color: #f39c12; font-weight: bold; }
    .churn-low { color: #2ecc71; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_predictor():
    return ChurnPredictor()

def main():
    st.title("🛒 E-Commerce Customer Churn Predictor")
    st.markdown("Predict the likelihood of a customer leaving based on their transaction history.")
    
    try:
        predictor = load_predictor()
    except Exception as e:
        st.error(f"Error loading model: {e}. Please ensure you are running from the project root.")
        return

    # Create layout
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.header("Customer Profile")
        with st.form("customer_input_form"):
            st.subheader("RFM Metrics")
            recency = st.slider("Recency (Days since last purchase)", 0, 365, 45)
            frequency = st.number_input("Frequency (Total Invoices)", 1, 100, 5)
            monetary = st.number_input("Total Spent (£)", 0.0, 10000.0, 500.0)
            
            st.subheader("Behavioral Metrics")
            purchases_30d = st.slider("Purchases in Last 30 Days", 0, 20, 1)
            lifetime_days = st.slider("Customer Lifetime (Days)", 1, 500, 180)
            avg_days_between = st.slider("Avg Days Between Purchases", 0, 100, 30)
            
            st.subheader("Product Metrics")
            unique_products = st.number_input("Unique Products Bought", 1, 500, 20)
            avg_order_val = monetary / frequency if frequency > 0 else 0
            st.info(f"Calculated Avg Order Value: £{avg_order_val:.2f}")
            
            submit_button = st.form_submit_button("Predict Churn Risk")

    with col2:
        if submit_button:
            st.header("Prediction Results")
            
            # Prepare data dict
            customer_data = {
                'Recency': recency,
                'Frequency': frequency,
                'TotalSpent': monetary,
                'AvgOrderValue': avg_order_val,
                'UniqueProducts': unique_products,
                'TotalItems': frequency * 3,  # Estimate for demo
                'AvgDaysBetweenPurchases': avg_days_between,
                'Purchases_Last30Days': purchases_30d,
                'CustomerLifetimeDays': lifetime_days
            }
            
            with st.spinner("Analyzing customer data..."):
                result = predictor.predict(customer_data)
                
            prob = result['churn_probability']
            risk = result['risk_level']
            
            # Gauge Chart for Probability
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = prob * 100,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Churn Probability (%)"},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkblue"},
                    'steps' : [
                        {'range': [0, 40], 'color': "lightgreen"},
                        {'range': [40, 75], 'color': "gold"},
                        {'range': [75, 100], 'color': "salmon"}],
                    'threshold' : {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90}
                }
            ))
            st.plotly_chart(fig, use_container_width=True)
            
            # Risk Level and Action
            if risk == "High":
                st.error(f"🚨 **HIGH RISK** - immediate action required.")
                st.markdown("**Recommended Action:** Trigger a VIP retention call and offer a 20% discount on their most browsed category. Send a customized 'We miss you' email.")
            elif risk == "Medium":
                st.warning(f"⚠️ **MEDIUM RISK** - monitor closely.")
                st.markdown("**Recommended Action:** Enroll in automated re-engagement campaign with a standard 10% win-back voucher valid for 7 days.")
            else:
                st.success(f"✅ **LOW RISK** - healthy customer.")
                st.markdown("**Recommended Action:** Maintain standard marketing cadence. Do not use discounts; preserve margin.")
                
            # Explainability Section
            st.subheader("Key Drivers for this Prediction")
            
            drivers = []
            if recency > 90:
                drivers.append("🔴 **High Recency:** Customer hasn't purchased recently.")
            elif recency < 30:
                drivers.append("🟢 **Low Recency:** Recent purchase activity lowers risk.")
                
            if purchases_30d == 0:
                drivers.append("🔴 **Zero momentum:** No purchases in the last 30 days strongly signals fading interest.")
            else:
                drivers.append(f"🟢 **Healthy momentum:** {purchases_30d} purchases in last 30 days is a protective factor.")
                
            if frequency == 1:
                drivers.append("🔴 **One-time buyer:** Failed to transition to repeat customer.")
                
            for driver in drivers:
                st.markdown(driver)

        else:
            st.info("👈 Enter customer metrics in the sidebar and click 'Predict Churn Risk' to see the analysis.")
            st.image("https://img.freepik.com/free-vector/customer-retention-concept-illustration_114360-6316.jpg", width=400)

if __name__ == "__main__":
    main()
