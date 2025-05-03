
import streamlit as st
import pandas as pd
import plotly.express as px
import random
import io
from lifelines import KaplanMeierFitter
from sklearn.ensemble import RandomForestClassifier

# --- Helper Functions ---

def download_csv(dataframe, filename="installed_base_data.csv"):
    csv = dataframe.to_csv(index=False)
    st.download_button(
        label="Download Data as CSV",
        data=csv,
        file_name=filename,
        mime="text/csv",
    )

def predict_maintenance(data):
    threshold = 10000
    data['Needs Maintenance'] = data['Usage Hours'] > threshold
    return data

def render_usage_trends(data):
    if "ds" in data.columns and "Usage Hours" in data.columns:
        fig = px.line(data, x="ds", y="Usage Hours", title="Usage Hours Over Time")
        st.plotly_chart(fig)
    else:
        st.warning("No time-series column (`ds`) found for usage trends.")

def render_revenue_forecast(data):
    with st.expander("💰 Revenue Forecast (Entitlement-Driven)", expanded=False):
        st.markdown("This section estimates future revenue based on expected usage (entitlement) and average revenue per usage hour.")
        if "Entitled Usage" not in data.columns:
            st.warning("Entitlement data not found. Run the Installed Base module first.")
            return

        avg_revenue_per_hour = st.number_input("Average Aftermarket Revenue per Hour ($)", value=15.0)
        forecast_years = st.slider("Forecast Horizon (Years)", 1, 5, 3)

        annual_hours = 2000
        forecast_data = data.copy()
        forecast_data["Forecasted Annual Usage"] = forecast_data["Entitled Usage"] * forecast_data["Utilization %"] / 100
        forecast_data["Annual Revenue"] = forecast_data["Forecasted Annual Usage"] * avg_revenue_per_hour
        forecast_data["Total Forecast Revenue"] = forecast_data["Annual Revenue"] * forecast_years

        st.dataframe(forecast_data[["Equipment ID", "Forecasted Annual Usage", "Annual Revenue", "Total Forecast Revenue"]], use_container_width=True)

        total_revenue = forecast_data["Total Forecast Revenue"].sum()
        avg_revenue = forecast_data["Annual Revenue"].mean()

        st.metric("Total Forecasted Revenue", f"${total_revenue:,.0f}")
        st.metric("Average Annual Revenue per Unit", f"${avg_revenue:,.0f}")

        fig_rev = px.bar(forecast_data, x="Equipment ID", y="Total Forecast Revenue",
                        title="Revenue Forecast per Equipment",
                        labels={"Total Forecast Revenue": "Revenue ($)"})
        st.plotly_chart(fig_rev, use_container_width=True)

def render_ai_insights(data):
    with st.expander("🤖 AI-Powered Business Insights", expanded=False):
        st.markdown("This section uses a simple machine learning model to predict the likelihood of maintenance needs based on usage and location patterns.")

        if "Needs Maintenance" not in data.columns:
            st.warning("Run the maintenance check first.")
            return

        # Basic encoding
        df = data.copy()
        df["Location_Code"] = df["Location"].astype("category").cat.codes
        df["Service_History_Code"] = df["Service History"].astype("category").cat.codes

        features = df[["Usage Hours", "Location_Code", "Service_History_Code"]]
        target = df["Needs Maintenance"]

        model = RandomForestClassifier(n_estimators=10, random_state=42)
        model.fit(features, target)

        feature_importance = pd.DataFrame({
            "Feature": features.columns,
            "Importance": model.feature_importances_
        }).sort_values(by="Importance", ascending=False)

        st.write("### 🔍 Feature Importance")
        st.dataframe(feature_importance, use_container_width=True)

        st.write("Model indicates which factors most influence the need for maintenance.")
