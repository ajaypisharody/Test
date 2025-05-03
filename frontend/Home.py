import streamlit as st
import pandas as pd
import sys, os

# Path setup
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Streamlit config
st.set_page_config(page_title="Insiful | LYZE", layout="wide")

# ======== STYLING AND COMPONENT IMPORTS ======== #
from components.sidebar import render_sidebar
from components.topbar import render_topbar

# Hide default Streamlit menu and footer
st.markdown("""
    <style>
        #MainMenu, footer {visibility: hidden;}
        .block-container { padding-top: 1.5rem; padding-bottom: 1rem; }
        .app-header {
            font-size: 28px;
            font-weight: 600;
            color: #1F2937;
            margin-bottom: 1rem;
            font-family: 'Segoe UI', sans-serif;
        }
        .metric-card {
            background: #F9FAFB;
            border: 1px solid #E5E7EB;
            border-radius: 12px;
            padding: 1.25rem;
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

# ========== STATEFUL NAVIGATION ========== #
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

def navigate(page_name):
    st.session_state.current_page = page_name
    st.experimental_rerun()

# ========== UI LAYOUT ========== #
render_topbar()
render_sidebar(navigate)

# ========== HOME PAGE ========== #
if st.session_state.current_page == "Home":
    st.markdown('<div class="app-header">📊 LYZE - AI Analytics</div>', unsafe_allow_html=True)
    st.markdown("Welcome to your enterprise analytics suite. Upload data and click a module to get started.")

    st.markdown("#### 📁 Upload Installed Base CSV")
    uploaded_file = st.file_uploader("Upload CSV with columns like `Equipment ID`, `Location`, `Usage Hours`, etc.", type=["csv"])

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

    # ======== MODULES GRID ======== #
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📦 Installed Base", key="nav1"):
            navigate("Installed Base")
        st.markdown('<div class="metric-card">View equipment footprint and service data.</div>', unsafe_allow_html=True)

    with col2:
        if st.button("📈 Revenue Forecast", key="nav2"):
            navigate("Revenue Forecast")
        st.markdown('<div class="metric-card">Time series forecast for revenue planning.</div>', unsafe_allow_html=True)

    with col3:
        if st.button("⚙️ Parts Demand", key="nav3"):
            navigate("Parts Demand")
        st.markdown('<div class="metric-card">Predict service part consumption intelligently.</div>', unsafe_allow_html=True)

    col4, col5, _ = st.columns([1,1,1])
    with col4:
        if st.button("💰 Opportunity Engine", key="nav4"):
            navigate("Opportunity Engine")
        st.markdown('<div class="metric-card">Identify churn risks and upsell opportunities.</div>', unsafe_allow_html=True)

    st.write("---")
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
