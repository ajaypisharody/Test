# home.py
import streamlit as st
import pandas as pd
import sys, os

# Path setup
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import reusable UI components
from components.sidebar import render_sidebar
from components.topbar import render_topbar

# Streamlit config
st.set_page_config(page_title="Insiful | LYZE", layout="wide")

# Top navigation and sidebar
render_topbar()
render_sidebar()

# Session state for page navigation
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

def navigate(page_name):
    st.session_state.current_page = page_name
    st.experimental_rerun()

# ========== HOME PAGE CONTENT ========== #
if st.session_state.current_page == "Home":
    st.markdown("""
    <style>
        .kpi-card {
            border: 1px solid #e0e0e0;
            border-radius: 12px;
            padding: 1rem;
            background-color: #ffffff;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
        }
        .kpi-title {
            font-size: 16px;
            color: #7f8c8d;
            margin-bottom: 5px;
        }
        .kpi-value {
            font-size: 24px;
            font-weight: 600;
            color: #2c3e50;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("## Dashboard Overview")
    st.markdown("Welcome to your aftermarket intelligence dashboard. Upload Installed Base data to activate modules.")

    st.markdown("#### Upload Installed Base CSV")
    uploaded_file = st.file_uploader("Upload CSV file with columns like `Equipment ID`, `Location`, `Usage Hours`, etc.", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        required_cols = {"Equipment ID", "Location", "Usage Hours", "Service History", "Latitude", "Longitude", "ds"}

        if required_cols.issubset(df.columns):
            st.session_state["installed_base_data"] = df
            st.success("✅ Data uploaded successfully. All modules can now access this.")
            st.dataframe(df.head())
        else:
            st.error(f"❌ Missing required columns: {required_cols - set(df.columns)}")
    elif "installed_base_data" not in st.session_state:
        st.warning("⚠️ Please upload a valid CSV file to proceed with any module.")

    st.markdown("---")

    # KPI Cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class='kpi-card'>
            <div class='kpi-title'>5-Year Recurring Revenue</div>
            <div class='kpi-value'>$3,201,000</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='kpi-card'>
            <div class='kpi-title'>5-Year Service Revenue</div>
            <div class='kpi-value'>$1,000,500</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class='kpi-card'>
            <div class='kpi-title'>Propensity to Buy (Avg)</div>
            <div class='kpi-value'>90%</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Module Navigation
    st.subheader("Modules")
    col4, col5, col6 = st.columns(3)
    with col4:
        if st.button("📦 Installed Base"):
            navigate("Installed Base")

    with col5:
        if st.button("📈 Revenue Forecast"):
            navigate("Revenue Forecast")

    with col6:
        if st.button("⚙️ Parts Demand"):
            navigate("Parts Demand")

    col7, _ = st.columns([1, 2])
    with col7:
        if st.button("💰 Opportunity Engine"):
            navigate("Opportunity Engine")

    st.markdown("---")
    st.caption("© 2025 Aftermarket AI — All rights reserved.")

# ========== PAGE ROUTING ========== #
elif st.session_state.current_page == "Installed Base":
    from pages.installed_base import render_installed_base
    render_installed_base()

elif st.session_state.current_page == "Revenue Forecast":
    from pages.forecasting import render_forecasting
    render_forecasting()

elif st.session_state.current_page == "Parts Demand":
    from pages.parts_inventory import render_parts_inventory
    render_parts_inventory()

elif st.session_state.current_page == "Opportunity Engine":
    from pages.opportunity_engine import render_opportunities
    render_opportunities()

elif st.session_state.current_page == "Auth":
    from pages.auth import render_auth
    render_auth()
