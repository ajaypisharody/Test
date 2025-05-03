import streamlit as st
import pandas as pd
import plotly.express as px
import random
from lifelines import KaplanMeierFitter

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

def to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False)
    return output.getvalue()

def render_usage_trends(data):
    if "ds" in data.columns and "Usage Hours" in data.columns:
        fig = px.line(data, x="ds", y="Usage Hours", title="Usage Hours Over Time")
        st.plotly_chart(fig)
    else:
        st.warning("No time-series column (`ds`) found for usage trends.")

def render_revenue_forecast(data):
    st.subheader("💰 Revenue Forecast (Entitlement-Driven)")

    if "Entitled Usage" not in data.columns:
        st.warning("Entitlement data not found. Run the Installed Base module first.")
        return

    avg_revenue_per_hour = st.number_input("Average Aftermarket Revenue per Hour ($)", value=15.0)
    forecast_years = st.slider("Forecast Horizon (Years)", 1, 5, 3)

    # Assume 250 working days per year * 8 hours = 2000
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

# --- Main Render Function ---
def render_installed_base():
    st.title("📦 Installed Base Intelligence")

    if st.button("🔙 Back to Home"):
        st.session_state.current_page = "Home"
        st.experimental_rerun()

    if "installed_base_data" not in st.session_state:
        st.error("❌ No data uploaded. Please return to Home and upload Installed Base data.")
        return

    data = st.session_state.installed_base_data

    st.markdown("""
        Gain insights into your equipment base. This module helps visualize, filter, and analyze 
        your installed base with detailed metrics and interactive visuals.
    """)

    st.subheader("Raw Data Preview")
    st.dataframe(data.head(), use_container_width=True)

    required_cols = ["Equipment ID", "Location", "Usage Hours", "Service History"]
    missing = [col for col in required_cols if col not in data.columns]
    if missing:
        st.error(f"❌ Missing required columns: {', '.join(missing)}")
        return

    data = predict_maintenance(data)

    st.subheader("🔧 Maintenance Dashboard")
    maintenance_data = data[data['Needs Maintenance']]
    if maintenance_data.empty:
        st.success("✅ All equipment is within usage threshold.")
    else:
        st.warning(f"⚠️ {maintenance_data.shape[0]} units require maintenance.")
        st.dataframe(maintenance_data[["Equipment ID", "Usage Hours", "Location", "Service History"]])

    st.subheader("📍 Equipment Distribution by Location")
    location_counts = data["Location"].value_counts()
    fig1 = px.bar(location_counts, x=location_counts.index, y=location_counts.values,
                  labels={'x': 'Location', 'y': 'Count'})
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("📊 Usage Hours Distribution")
    fig2 = px.histogram(data, x="Usage Hours", nbins=20)
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("🛠️ Service History Breakdown")
    service_counts = data["Service History"].value_counts()
    fig3 = px.pie(service_counts, names=service_counts.index, values=service_counts.values)
    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("🔍 Filter Data")
    location_filter = st.multiselect("Location", options=data["Location"].unique(), default=data["Location"].unique())
    service_filter = st.multiselect("Service History", options=data["Service History"].unique(), default=data["Service History"].unique())
    filtered = data[data["Location"].isin(location_filter) & data["Service History"].isin(service_filter)]

    st.write(f"Showing {filtered.shape[0]} records")
    st.dataframe(filtered, use_container_width=True)

    download_csv(filtered)

    st.subheader("📈 Summary Metrics")
    st.metric("Total Units", f"{filtered.shape[0]}")
    st.metric("Avg Usage Hours", f"{filtered['Usage Hours'].mean():,.2f}")
    st.metric("Top Location", filtered['Location'].value_counts().idxmax())
    st.metric("Most Common Service History", filtered['Service History'].value_counts().idxmax())

    st.subheader("🔬 Usage by Equipment")
    usage_by_equipment = filtered.groupby("Equipment ID")["Usage Hours"].sum().reset_index()
    fig4 = px.bar(usage_by_equipment, x="Equipment ID", y="Usage Hours", title="Usage by Equipment")
    st.plotly_chart(fig4, use_container_width=True)

    st.subheader("📆 Historical Usage Trends")
    render_usage_trends(filtered)

    st.subheader("📐 Entitlement Calculator")
    method = st.radio("Choose Entitlement Calculation Method:", ["Peer Benchmarking", "Kaplan-Meier Survival Analysis"])

    if method == "Kaplan-Meier Survival Analysis":
        if "Lifetime Hours" not in data.columns:
            data["Lifetime Hours"] = data["Usage Hours"] + random.randint(1000, 5000)
            data["Observed"] = 1

        kmf = KaplanMeierFitter()
        kmf.fit(durations=data["Lifetime Hours"], event_observed=data["Observed"])

        st.markdown("Estimated survival function using Kaplan-Meier method:")
        survival_df = pd.DataFrame({"Hours": kmf.survival_function_.index, "Survival Probability": kmf.survival_function_["KM_estimate"]})
        fig_surv = px.line(survival_df, x="Hours", y="Survival Probability", title="Kaplan-Meier Survival Curve")
        st.plotly_chart(fig_surv, use_container_width=True)

        # Manually calculate quantiles from survival function
        median_lifecycle = survival_df[survival_df["Survival Probability"] >= 0.5].iloc[0]["Hours"]
        q25_lifecycle = survival_df[survival_df["Survival Probability"] >= 0.25].iloc[0]["Hours"]
        q75_lifecycle = survival_df[survival_df["Survival Probability"] >= 0.75].iloc[0]["Hours"]

        st.metric("Median Lifecycle (50%)", f"{median_lifecycle:.0f} hrs")
        st.metric("25% Lifecycle", f"{q25_lifecycle:.0f} hrs")
        st.metric("75% Lifecycle", f"{q75_lifecycle:.0f} hrs")

        data["Entitled Usage"] = median_lifecycle  # Use median lifecycle for entitlement

    else:
        entitled_hours = data["Usage Hours"].median() * 1.2
        data["Entitled Usage"] = entitled_hours
        st.metric("Benchmark Entitlement (120% of median)", f"{entitled_hours:.0f} hrs")

    data["Utilization %"] = (data["Usage Hours"] / data["Entitled Usage"]) * 100
    data["Utilization Flag"] = data["Utilization %"].apply(lambda x: "Overused" if x > 120 else ("Underused" if x < 80 else "Optimal"))

    st.dataframe(data[["Equipment ID", "Usage Hours", "Entitled Usage", "Utilization %", "Utilization Flag"]], use_container_width=True)

    fig5 = px.bar(data, x="Equipment ID", y=["Usage Hours", "Entitled Usage"],
                  barmode="group", title="Actual vs Entitled Usage",
                  labels={"value": "Hours", "variable": "Type"})
    st.plotly_chart(fig5, use_container_width=True)

    flag_counts = data["Utilization Flag"].value_counts()
    st.metric("Underused Units", int(flag_counts.get("Underused", 0)))
    st.metric("Overused Units", int(flag_counts.get("Overused", 0)))
    st.metric("Optimal Units", int(flag_counts.get("Optimal", 0)))

    st.session_state.entitlement_data = data[["Equipment ID", "Entitled Usage", "Utilization %", "Utilization Flag"]]

    render_revenue_forecast(data)

    st.success("✅ Installed Base Module Loaded.")
