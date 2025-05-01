import streamlit as st
import pandas as pd
import plotly.express as px
import io

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

# --- Main Render Function ---
def render_installed_base():
    st.title("📦 Installed Base Intelligence")

    # Navigation
    if st.button("🔙 Back to Home"):
        st.session_state.current_page = "Home"
        st.experimental_rerun()

    # Ensure data was uploaded
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

    # Validate required columns
    required_cols = ["Equipment ID", "Location", "Usage Hours", "Service History"]
    missing = [col for col in required_cols if col not in data.columns]
    if missing:
        st.error(f"❌ Missing required columns: {', '.join(missing)}")
        return

    # Predict Maintenance
    data = predict_maintenance(data)

    # Maintenance Alerts
    st.subheader("🔧 Maintenance Dashboard")
    maintenance_data = data[data['Needs Maintenance']]
    if maintenance_data.empty:
        st.success("✅ All equipment is within usage threshold.")
    else:
        st.warning(f"⚠️ {maintenance_data.shape[0]} units require maintenance.")
        st.dataframe(maintenance_data[["Equipment ID", "Usage Hours", "Location", "Service History"]])

    # Location Distribution
    st.subheader("📍 Equipment Distribution by Location")
    location_counts = data["Location"].value_counts()
    fig1 = px.bar(location_counts, x=location_counts.index, y=location_counts.values,
                  labels={'x': 'Location', 'y': 'Count'})
    st.plotly_chart(fig1, use_container_width=True)

    # Usage Hours Histogram
    st.subheader("📊 Usage Hours Distribution")
    fig2 = px.histogram(data, x="Usage Hours", nbins=20)
    st.plotly_chart(fig2, use_container_width=True)

    # Service History Breakdown
    st.subheader("🛠️ Service History Breakdown")
    service_counts = data["Service History"].value_counts()
    fig3 = px.pie(service_counts, names=service_counts.index, values=service_counts.values)
    st.plotly_chart(fig3, use_container_width=True)

    # Filters
    st.subheader("🔍 Filter Data")
    location_filter = st.multiselect("Location", options=data["Location"].unique(), default=data["Location"].unique())
    service_filter = st.multiselect("Service History", options=data["Service History"].unique(), default=data["Service History"].unique())
    filtered = data[data["Location"].isin(location_filter) & data["Service History"].isin(service_filter)]

    st.write(f"Showing {filtered.shape[0]} records")
    st.dataframe(filtered, use_container_width=True)

    # Download Button
    download_csv(filtered)

    # Summary Metrics
    st.subheader("📈 Summary Metrics")
    st.metric("Total Units", f"{filtered.shape[0]}")
    st.metric("Avg Usage Hours", f"{filtered['Usage Hours'].mean():,.2f}")
    st.metric("Top Location", filtered['Location'].value_counts().idxmax())
    st.metric("Most Common Service History", filtered['Service History'].value_counts().idxmax())

    # Equipment-Level Breakdown
    st.subheader("🔬 Usage by Equipment")
    usage_by_equipment = filtered.groupby("Equipment ID")["Usage Hours"].sum().reset_index()
    fig4 = px.bar(usage_by_equipment, x="Equipment ID", y="Usage Hours", title="Usage by Equipment")
    st.plotly_chart(fig4, use_container_width=True)

    # Time Series Chart (optional)
    st.subheader("📆 Historical Usage Trends")
    render_usage_trends(filtered)

    st.success("✅ Installed Base Module Loaded.")
