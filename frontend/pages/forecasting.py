import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import numpy as np
import io
from datetime import datetime

def render_forecasting():
    st.title("📈 Aftermarket Revenue Forecasting")

    # Navigation
    if st.button("🔙 Back to Home"):
        st.session_state.current_page = "Home"
        st.experimental_rerun()

    # Load Installed Base data from session
    installed_base = st.session_state.get("installed_base_data", None)

    if installed_base is None:
        st.warning("Please upload Installed Base data on the Home page first.")
        return

    st.success("✅ Installed Base data loaded from Home page.")

    # Upload revenue data
    st.subheader("📂 Upload Aftermarket Revenue Data")
    revenue_file = st.file_uploader("Upload CSV containing revenue transactions (with Equipment ID & Date)", type=["csv"])

    if revenue_file:
        revenue_data = pd.read_csv(revenue_file)

        # Ensure date column is datetime
        if 'Date' in revenue_data.columns:
            revenue_data['Date'] = pd.to_datetime(revenue_data['Date'])
        else:
            st.error("Revenue dataset must include a 'Date' column.")
            return

        # Merge with installed base on Equipment ID
        merged = pd.merge(revenue_data, installed_base, on="Equipment ID", how="left")

        st.write("### Merged Revenue & Equipment Data")
        st.dataframe(merged.head(), use_container_width=True)

        # Show revenue trends
        st.subheader("📊 Revenue Trends Over Time")
        rev_trend = merged.groupby(merged['Date'].dt.to_period('M')).sum().reset_index()
        rev_trend['Date'] = rev_trend['Date'].dt.to_timestamp()

        fig = px.line(rev_trend, x='Date', y='Revenue', title='Total Revenue Over Time')
        st.plotly_chart(fig, use_container_width=True)

        # Correlation check: Usage Hours vs Revenue
        st.subheader("📉 Correlation: Usage Hours vs Revenue")
        usage_vs_rev = merged[['Usage Hours', 'Revenue']].dropna()
        fig2 = px.scatter(usage_vs_rev, x='Usage Hours', y='Revenue', trendline="ols")
        st.plotly_chart(fig2, use_container_width=True)

        # Forecasting using Linear Regression (for simplicity)
        st.subheader("📈 Forecast Future Revenue")

        forecast_df = merged.copy()
        forecast_df['Month'] = forecast_df['Date'].dt.to_period("M").dt.to_timestamp()
        monthly_rev = forecast_df.groupby("Month")["Revenue"].sum().reset_index()

        # Feature engineering for linear regression
        monthly_rev["Month_Num"] = np.arange(len(monthly_rev))
        X = monthly_rev[["Month_Num"]]
        y = monthly_rev["Revenue"]

        model = LinearRegression()
        model.fit(X, y)

        # Predict next 6 months
        future_months = pd.date_range(monthly_rev['Month'].max(), periods=7, freq='M')[1:]
        future_df = pd.DataFrame({
            "Month": future_months,
            "Month_Num": np.arange(len(monthly_rev), len(monthly_rev) + 6)
        })
        future_df["Forecast"] = model.predict(future_df[["Month_Num"]])

        forecast_result = pd.concat([
            monthly_rev[["Month", "Revenue"]].rename(columns={"Revenue": "Actual Revenue"}),
            future_df[["Month", "Forecast"]]
        ], axis=0).reset_index(drop=True)

        fig3 = px.line(forecast_result, x="Month", y=["Actual Revenue", "Forecast"],
                       title="Revenue Forecast (Next 6 Months)")
        st.plotly_chart(fig3, use_container_width=True)

        # Error metric display
        predictions = model.predict(X)
        rmse = np.sqrt(mean_squared_error(y, predictions))
        st.metric(label="Model RMSE", value=f"${rmse:,.2f}")

        # Export forecast
        st.download_button(
            label="📥 Download Forecast as CSV",
            data=forecast_result.to_csv(index=False),
            file_name="revenue_forecast.csv",
            mime="text/csv"
        )

    else:
        st.info("Please upload a revenue dataset to proceed with forecasting.")
