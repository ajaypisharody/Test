import streamlit as st
import pandas as pd
from ml_models.forecasting import forecast_revenue

def render_forecasting():
    st.subheader("Predictive Revenue Forecasting")
    st.info("Upload a CSV with columns `ds` and `y`.")
    uploaded_file = st.file_uploader("Upload Revenue Data", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write("Uploaded Data", df.head())

        if "ds" in df.columns and "y" in df.columns:
            forecast = forecast_revenue(df)
            st.line_chart(forecast[["ds", "yhat"]].set_index("ds"))
            st.success("Revenue forecast complete!")
        else:
            st.error("Uploaded file must have `ds` and `y` columns.")
