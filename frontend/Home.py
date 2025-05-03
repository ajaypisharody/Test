import streamlit as st
import pandas as pd
import sys, os

# Path setup
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Streamlit config
st.set_page_config(page_title="Insiful | LYZE", layout="wide")

# ========== STYLES ========== #
st.markdown("""
    <style>
        #MainMenu, footer {visibility: hidden;}
        .block-container { padding-top: 2rem; }

        .app-header {
            font-size: 36px;
            font-weight: 600;
            color: #1A1A1A;
            padding-bottom: 2rem;
            text-align: left;
            font-family: 'Segoe UI', sans-serif;
            border-bottom: 1px solid #DDD;
            margin-bottom: 2rem;
        }

        .metric-card {
            border: 1px solid #DDD;
            border-radius: 10px;
            padding: 1.25rem;
            background-color: #FAFAFA;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
            text-align: left;
            font-family: 'Segoe UI', sans-serif;
            transition: all 0.2s ease;
            height: 90px;
            font-size: 14px;
            color: #333;
        }

        .metric-card:hover {
            background-color: #F5F5F5;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            cursor: pointer;
        }

        .top-right-button {
            position: fixed;
            top: 20px;
            right: 30px;
            z-index: 999;
        }

        .top-right-button button {
            background-color: #004080;
            color: #FFFFFF;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            font-size: 14px;
            font-weight: 500;
            font-family: 'Segoe UI', sans-serif;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
            transition: 0.3s ease;
        }

        .top-right-button button:hover {
            background-color: #002D5A;
        }
    </style>

    <div class="top-right-button">
        <form action="">
            <button onclick="window.location.reload();" class="stButton">🔐 Login / Signup</button>
        </form>
    </div>
""", unsafe_allow_html=True)

# ========== SESSION STATE SETUP ========== #
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

def navigate(page_name):
    st.session_state.current_page = page_name
    st.experimental_rerun()

# Dummy handler for login redirect
if st.button("🔐", key="auth_topright", help="Login Hidden"):
    navigate("Auth")

# ========== HOME PAGE ========== #
if st.session_state.current_page == "Home":
    st.markdown('<div class="app-header">LYZE Analytics Suite</div>', unsafe_allow_html=True)
    st.markdown("Welcome to your AI-powered analytics platform. Upload Installed Base data to begin.")

    # Upload section
    st.markdown("#### 📁 Upload Installed Base CSV")
    uploaded_file = st.file_uploader("Upload a CSV with columns like `Equipment ID`, `Location`, `Usage Hours`, etc.", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        required_cols = {"Equipment ID", "Location", "Usage Hours", "Service History", "Latitude", "Longitude", "ds"}

        if required_cols.issubset(df.columns):
            st.session_state["installed_base_data"] = df
            st.success("✅ Data uploaded successfully. All modules are now enabled.")
            st.dataframe(df.head())
        else:
            st.error(f"❌ Missing required columns: {required_cols - set(df.columns)}")
    elif "installed_base_data" not in st.session_state:
        st.warning("⚠️ Please upload a valid CSV file to proceed.")

    # Module grid
    st.markdown("#### 🔍 Available Modules")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📦 Installed Base"):
            navigate("Installed Base")
        st.markdown('<div class="metric-card">Analyze your equipment footprint and lifecycle.</div>', unsafe_allow_html=True)

    with col2:
        if st.button("📈 Revenue Forecast"):
            navigate("Revenue Forecast")
        st.markdown('<div class="metric-card">Predict future aftermarket revenue trends.</div>', unsafe_allow_html=True)

    with col3:
        if st.button("⚙️ Parts Demand"):
            navigate("Parts Demand")
        st.markdown('<div class="metric-card">Forecast service parts demand using AI.</div>', unsafe_allow_html=True)

    col4, col5, _ = st.columns([1, 1, 1])
    with col4:
        if st.button("💰 Opportunity Engine"):
            navigate("Opportunity Engine")
        st.markdown('<div class="metric-card">Identify churn risks and upsell opportunities.</div>', unsafe_allow_html=True)

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
