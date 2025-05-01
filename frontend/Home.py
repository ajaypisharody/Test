import streamlit as st
import pandas as pd
import sys, os

# Path setup
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Streamlit config
st.set_page_config(page_title="Insiful | LYZE", layout="wide")

# Hide default Streamlit menu and footer
st.markdown("""
    <style>
        #MainMenu, footer {visibility: hidden;}
        .block-container { padding-top: 2rem; }
        .app-header {
            font-size: 30px;
            font-weight: bold;
            padding: 1rem 0 2rem 0;
        }
        .metric-card {
            border: 1px solid #ddd;
            border-radius: 12px;
            padding: 1.5rem;
            text-align: center;
            background-color: #f9f9f9;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
            height: 120px;
        }
        .metric-card:hover {
            background-color: #eef6ff;
            cursor: pointer;
            transition: 0.3s ease-in-out;
        }
    </style>
""", unsafe_allow_html=True)

# Session state for page navigation
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

def navigate(page_name):
    st.session_state.current_page = page_name
    st.experimental_rerun()

# ========== HOME PAGE ========== #
if st.session_state.current_page == "Home":
    st.markdown('<div class="app-header">📊 LYZE - AI Analytics</div>', unsafe_allow_html=True)
    st.markdown("Welcome to your enterprise analytics suite. Upload data and click a module to get started.")

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

    # Modules Grid
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

    st.write("")
    col4, col5 = st.columns(2)

    with col4:
        if st.button("💰 Opportunity Engine", key="nav4"):
            navigate("Opportunity Engine")
        st.markdown('<div class="metric-card">Identify churn risks and upsell opportunities.</div>', unsafe_allow_html=True)

    with col5:
        if st.button("🔐 Login / Signup", key="nav5"):
            navigate("Auth")
        st.markdown('<div class="metric-card">Enterprise-grade authentication module.</div>', unsafe_allow_html=True)

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
