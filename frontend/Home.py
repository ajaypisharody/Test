import streamlit as st
import pandas as pd
import sys, os

# Path setup
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Streamlit config
st.set_page_config(page_title="Insiful | LYZE", layout="wide")

# ======== CUSTOM COMPONENT IMPORTS ======== #
from components.topbar import render_topbar
from components.sidebar import render_sidebar

# ======== HIDE NATIVE NAVIGATION ======== #
st.markdown("""
    <style>
        #MainMenu, footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container { padding-top: 2rem; padding-bottom: 1rem; }
        .app-header {
            font-size: 30px;
            font-weight: 600;
            color: #1F2937;
            margin-bottom: 1.5rem;
            font-family: 'Segoe UI', sans-serif;
        }
        .metric-card {
            background: #F9FAFB;
            border: 1px solid #E5E7EB;
            border-radius: 12px;
            padding: 1rem 1.25rem;
            text-align: left;
            box-shadow: 0 1px 3px rgba(0,0,0,0.06);
            transition: 0.2s ease;
            font-family: 'Segoe UI', sans-serif;
            height: 130px;
        }
        .metric-card:hover {
            background-color: #F3F4F6;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        }
    </style>
""", unsafe_allow_html=True)

# ======== STATEFUL ROUTING ======== #
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

def navigate(page_name):
    st.session_state.current_page = page_name
    st.rerun()

# ======== TOP BAR AND SIDEBAR ======== #
render_topbar()
render_sidebar(navigate)

# ======== HOME PAGE ======== #
if st.session_state.current_page == "Home":
    st.markdown('<div class="app-header">📊 LYZE - AI Analytics</div>', unsafe_allow_html=True)
    st.write("Welcome to your enterprise analytics suite. Upload data and click a module to get started.")

    # Upload CSV
    st.markdown("#### 📁 Upload Installed Base CSV")
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

    # ===== MODULE BUTTONS LAYOUT ===== #
    st.markdown("### 🔍 Explore Modules")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📦 Installed Base"):
            navigate("Installed Base")
        st.markdown('<div class="metric-card">View equipment footprint and service data.</div>', unsafe_allow_html=True)

    with col2:
        if st.button("📈 Revenue Forecast"):
            navigate("Revenue Forecast")
        st.markdown('<div class="metric-card">Time series forecast for revenue planning.</div>', unsafe_allow_html=True)

    with col3:
        if st.button("⚙️ Parts Demand"):
            navigate("Parts Demand")
        st.markdown('<div class="metric-card">Predict part consumption based on installed base.</div>', unsafe_allow_html=True)

    col4, col5, _ = st.columns([1, 1, 1])
    with col4:
        if st.button("💰 Opportunity Engine"):
            navigate("Opportunity Engine")
        st.markdown('<div class="metric-card">Identify upsell, cross-sell, and churn risks.</div>', unsafe_allow_html=True)

    st.write("---")
    st.caption("© 2025 Aftermarket AI — All rights reserved.")

# ======== PAGE ROUTING ======== #
elif st.session_state.current_page == "Installed Base":
    from modules.installed_base import render_installed_base
    render_installed_base()

elif st.session_state.current_page == "Revenue Forecast":
    from modules.forecasting import render_forecasting
    render_forecasting()

elif st.session_state.current_page == "Parts Demand":
    from modules.parts_inventory import render_parts_inventory
    render_parts_inventory()

elif st.session_state.current_page == "Opportunity Engine":
    from modules.opportunity_engine import render_opportunities
    render_opportunities()

elif st.session_state.current_page == "Auth":
    from modules.auth import render_auth
    render_auth()
