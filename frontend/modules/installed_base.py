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
    st.download_button("Download Filtered Data", data=csv, file_name=filename, mime="text/csv")

def detect_outliers_zscore(df, column):
    z = stats.zscore(df[column])
    return abs(z) > 3

def detect_outliers_iqr(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    return (df[column] < Q1 - 1.5 * IQR) | (df[column] > Q3 + 1.5 * IQR)

def industry_profile(data):
    st.subheader("🏭 Industry Detection & Profile")
    industry = data["Application"].mode()[0] if "Application" in data.columns else "General"
    st.markdown(f"**Detected Industry**: `{industry}` based on dominant application type")
    return industry

def predict_maintenance(data):
    threshold = data["Usage Hours"].quantile(0.95)
    data['Needs Maintenance'] = data['Usage Hours'] > threshold
    return data

def run_kaplan_meier(data):
    data["Event"] = data["Service History"].apply(lambda x: 1 if "failure" in str(x).lower() else 0)
    data["Lifetime"] = data["Usage Hours"]
    kmf = KaplanMeierFitter()
    kmf.fit(durations=data["Lifetime"], event_observed=data["Event"])

    st.markdown("**Kaplan-Meier Survival Estimate**")
    fig = px.line(kmf.survival_function_.reset_index(),
                  x="timeline", y="KM_estimate", title="Survival Curve")
    st.plotly_chart(fig)

    median_life = kmf.median_survival_time_
    st.metric("Median Lifecycle (50%)", f"{median_life:.0f} hrs")
    data["Entitled Usage"] = median_life
    return data

def run_ai_models(data):
    with st.expander("🤖 AI Models"):
        # Churn Classification
        st.subheader("Churn Prediction")
        data["Churn"] = data["Service History"].apply(lambda x: 0 if "none" in str(x).lower() else 1)
        features = ["Usage Hours", "Entitled Usage", "Utilization %"]
        churn_data = data.dropna(subset=features + ["Churn"])

        if not churn_data.empty:
            X = churn_data[features]
            y = churn_data["Churn"]
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
            model = RandomForestClassifier()
            model.fit(X_train, y_train)
            preds = model.predict(X_test)
            st.code(classification_report(y_test, preds), language='text')

        # Anomaly Detection
        st.subheader("Anomaly Detection")
        anomaly_features = ["Usage Hours", "Flow Rate", "Pressure", "Speed", "Temp Inlet"]
        valid = data.dropna(subset=anomaly_features)
        model = IsolationForest(contamination=0.1)
        valid["Anomaly Score"] = model.fit_predict(valid[anomaly_features])
        valid["Anomaly Label"] = valid["Anomaly Score"].map({-1: "Anomaly", 1: "Normal"})
        fig = px.scatter(valid, x="Usage Hours", y="Flow Rate", color="Anomaly Label",
                         title="Usage vs Flow Rate Anomalies")
        st.plotly_chart(fig)

def render_revenue_forecast(data):
    st.subheader("💰 Revenue Forecast")
    if "Entitled Usage" not in data.columns:
        st.warning("Entitled usage not available.")
        return
    avg_revenue = st.number_input("Revenue per Hour ($)", value=15.0)
    horizon = st.slider("Forecast Years", 1, 5, 3)
    data["Forecasted Usage"] = data["Entitled Usage"] * data["Utilization %"] / 100
    data["Forecasted Revenue"] = data["Forecasted Usage"] * avg_revenue * horizon
    st.metric("Total Forecast Revenue", f"${data['Forecasted Revenue'].sum():,.0f}")
    st.plotly_chart(px.bar(data, x="Equipment ID", y="Forecasted Revenue"))

# --- Main Function ---

def render_installed_base():
    st.title("📦 Installed Base Intelligence")

    if st.button("🔙 Back to Home"):
        st.session_state.current_page = "Home"
        st.rerun()

    if "installed_base_data" not in st.session_state:
        st.error("Please upload Installed Base data.")
        return

    data = st.session_state.installed_base_data
    st.dataframe(data.head(), use_container_width=True)

    required = ["Equipment ID", "Location", "Usage Hours", "Service History"]
    if any(col not in data.columns for col in required):
        st.error("Missing columns: " + ", ".join([c for c in required if c not in data.columns]))
        return

    industry = industry_profile(data)
    data = predict_maintenance(data)

    # Equipment Overview
    with st.expander("📊 Equipment Overview"):
        st.plotly_chart(px.histogram(data, x="Usage Hours"))
        st.plotly_chart(px.pie(data, names="Service History", title="Service Distribution"))
        #st.plotly_chart(px.bar(data["Location"].value_counts().reset_index(),x=data.index, y="Location", title="Units per Location"))

    # Entitlement Estimation
    with st.expander("📐 Entitlement"):
        method = st.radio("Estimation Method", ["Kaplan-Meier", "Statistical"])
        if method == "Kaplan-Meier":
            data = run_kaplan_meier(data)
        else:
            median = data["Usage Hours"].median() * 1.2
            data["Entitled Usage"] = median
            st.metric("Statistical Entitlement", f"{median:.0f} hrs")

        data["Utilization %"] = (data["Usage Hours"] / data["Entitled Usage"]) * 100
        z = stats.zscore(data["Utilization %"].fillna(0))
        data["Utilization Flag"] = ["Overused" if x > 1.5 else "Underused" if x < -1.5 else "Optimal" for x in z]
        st.dataframe(data[["Equipment ID", "Usage Hours", "Entitled Usage", "Utilization %", "Utilization Flag"]])

    # Technical Stats & Export
    with st.expander("⚙️ Engineering Parameters"):
        for col in ["Temp Inlet", "Temp Outlet", "Flow Rate", "Pressure", "Speed"]:
            if col in data.columns:
                st.plotly_chart(px.box(data, y=col, title=f"{col} Distribution"))
                outliers = detect_outliers_iqr(data, col)
                if outliers.any():
                    st.warning(f"{outliers.sum()} outliers detected in {col}")

    # Filter & Export
    with st.expander("📁 Export Filtered Data"):
        filters = st.multiselect("Application Type", data["Application"].unique(), default=data["Application"].unique())
        subset = data[data["Application"].isin(filters)]
        st.dataframe(subset, use_container_width=True)
        download_csv(subset)

    # AI + Revenue Forecast
    run_ai_models(data)
    render_revenue_forecast(data)

    st.session_state.entitlement_data = data
    st.success("✅ Analysis Complete.")

# Run only when called explicitly
if __name__ == "__main__" or "streamlit" in __name__:
    render_installed_base()
