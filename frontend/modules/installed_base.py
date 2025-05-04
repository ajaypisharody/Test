import streamlit as st
import pandas as pd
import plotly.express as px
from lifelines import KaplanMeierFitter
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from scipy import stats

# --- Helper Functions ---

def download_csv(dataframe, filename="installed_base_data.csv"):
    csv = dataframe.to_csv(index=False)
    st.download_button("Download Filtered Data as CSV", data=csv, file_name=filename, mime="text/csv")

def predict_maintenance(data):
    threshold = data["Usage Hours"].quantile(0.90)
    data['Needs Maintenance'] = data['Usage Hours'] > threshold
    return data

def run_kaplan_meier(data):
    data["Event"] = data["Service History"].apply(lambda x: 1 if "failure" in str(x).lower() else 0)
    data["Lifetime"] = data["Usage Hours"]
    kmf = KaplanMeierFitter()
    kmf.fit(durations=data["Lifetime"], event_observed=data["Event"])

    st.markdown("Estimated survival function using Kaplan-Meier method:")
    survival_df = kmf.survival_function_.reset_index()
    survival_df.columns = ["Hours", "Survival Probability"]
    fig = px.line(survival_df, x="Hours", y="Survival Probability", title="Kaplan-Meier Survival Curve")
    st.plotly_chart(fig)

    median_lifecycle = kmf.median_survival_time_
    st.metric("Median Lifecycle (50%)", f"{median_lifecycle:.0f} hrs")
    data["Entitled Usage"] = median_lifecycle
    return data

def run_ai_models(data):
    with st.expander("🤖 AI-Powered Insights"):
        st.markdown("This section uses machine learning to identify potential churn risks and usage anomalies across your installed base.")

        # Churn Prediction
        st.subheader("📉 Churn Prediction")
        data["Churn"] = data["Service History"].apply(lambda x: 0 if "none" in str(x).lower() else 1)
        feature_cols = ["Usage Hours", "Entitled Usage", "Utilization %"] + \
                       [col for col in data.columns if col.startswith("Temp") or col.startswith("Flow") or col in ["Pressure", "Speed"]]
        churn_data = data[feature_cols + ["Churn"]].dropna()
        X = churn_data.drop(columns=["Churn"])
        y = churn_data["Churn"]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        model = RandomForestClassifier()
        model.fit(X_train, y_train)
        preds = model.predict(X_test)

        st.markdown("**Model Evaluation Report:**")
        st.code(classification_report(y_test, preds), language='text')

    with st.expander("🚨 Anomaly Detection in Utilization"):
        st.markdown("Isolation Forest detects unusual utilization patterns.")
        iso_model = IsolationForest(contamination=0.1)
        data["Utilization %"] = data["Utilization %"].fillna(0)
        iso_preds = iso_model.fit_predict(data[["Utilization %"]])
        data["Anomaly Flag"] = ["Anomaly" if p == -1 else "Normal" for p in iso_preds]

        fig = px.scatter(data, x="Usage Hours", y="Utilization %", color="Anomaly Flag", title="Utilization Outliers")
        st.plotly_chart(fig)

def render_revenue_forecast(data):
    st.subheader("💰 Revenue Forecast (Entitlement-Driven)")
    if "Entitled Usage" not in data.columns:
        st.warning("Entitlement data not found.")
        return

    avg_revenue = st.number_input("Avg Aftermarket Revenue per Hour ($)", value=15.0)
    forecast_years = st.slider("Forecast Horizon (Years)", 1, 5, 3)

    data["Forecasted Annual Usage"] = data["Entitled Usage"] * data["Utilization %"] / 100
    data["Annual Revenue"] = data["Forecasted Annual Usage"] * avg_revenue
    data["Total Forecast Revenue"] = data["Annual Revenue"] * forecast_years

    st.metric("Total Forecasted Revenue", f"${data['Total Forecast Revenue'].sum():,.0f}")
    fig = px.bar(data, x="Equipment ID", y="Total Forecast Revenue", title="Forecast Revenue per Unit")
    st.plotly_chart(fig)

# --- Main Function ---
def render_installed_base():
    st.title("📦 Installed Base Intelligence")

    if st.button("🔙 Back to Home"):
        st.session_state.current_page = "Home"
        st.rerun()

    if "installed_base_data" not in st.session_state:
        st.error("❌ No data uploaded. Please return to Home and upload Installed Base data.")
        return

    data = st.session_state.installed_base_data
    st.dataframe(data.head(), use_container_width=True)

    required = ["Equipment ID", "Location", "Usage Hours", "Service History"]
    if any(col not in data.columns for col in required):
        st.error(f"Missing required columns: {', '.join([col for col in required if col not in data.columns])}")
        return

    data = predict_maintenance(data)

    with st.expander("📊 Equipment Insights"):
        tabs = st.tabs(["Usage", "Location", "Service", "Maintenance"])
        with tabs[0]:
            st.plotly_chart(px.histogram(data, x="Usage Hours", nbins=20))
        with tabs[1]:
            counts = data["Location"].value_counts()
            st.plotly_chart(px.bar(x=counts.index, y=counts.values, labels={"x": "Location", "y": "Count"}))
        with tabs[2]:
            svc_counts = data["Service History"].value_counts()
            st.plotly_chart(px.pie(values=svc_counts.values, names=svc_counts.index))
        with tabs[3]:
            flagged = data[data['Needs Maintenance']]
            if not flagged.empty:
                st.warning(f"{flagged.shape[0]} units exceed maintenance threshold.")
                st.dataframe(flagged[["Equipment ID", "Usage Hours", "Location"]])
            else:
                st.success("All units within usage limits.")

    with st.expander("📍 Filter & Export"):
        loc_filter = st.multiselect("Location", data["Location"].unique(), default=data["Location"].unique())
        svc_filter = st.multiselect("Service History", data["Service History"].unique(), default=data["Service History"].unique())
        filtered = data[data["Location"].isin(loc_filter) & data["Service History"].isin(svc_filter)]
        st.dataframe(filtered, use_container_width=True)
        download_csv(filtered)

    with st.expander("📐 Entitlement Calculator"):
        method = st.radio("Entitlement Method", ["Kaplan-Meier", "Statistical Benchmark"])
        if method == "Kaplan-Meier":
            data = run_kaplan_meier(data)
        else:
            benchmark = stats.trim_mean(data["Usage Hours"].dropna(), 0.1) * 1.1
            data["Entitled Usage"] = benchmark
            st.metric("Statistical Benchmark Entitlement", f"{benchmark:.0f} hrs")

        data["Utilization %"] = (data["Usage Hours"] / data["Entitled Usage"]) * 100
        z_scores = stats.zscore(data["Utilization %"].fillna(0))
        data["Utilization Flag"] = [
            "Underused" if z < -1 else "Overused" if z > 1 else "Optimal"
            for z in z_scores
        ]

        st.dataframe(data[["Equipment ID", "Usage Hours", "Entitled Usage", "Utilization %", "Utilization Flag"]])

    with st.expander("📊 Usage vs Entitlement"):
        st.plotly_chart(
            px.bar(data, x="Equipment ID", y=["Usage Hours", "Entitled Usage"], barmode="group", title="Actual vs Entitled Usage")
        )

    run_ai_models(data)
    render_revenue_forecast(data)

    st.session_state.entitlement_data = data[["Equipment ID", "Entitled Usage", "Utilization %", "Utilization Flag"]]
    st.success("✅ Installed Base Analysis Complete.")

# Run only when called explicitly
if __name__ == "__main__" or "streamlit" in __name__:
    render_installed_base()
