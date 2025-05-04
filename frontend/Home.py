import streamlit as st
import pandas as pd
import sys, os

# Path setup
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
st.set_page_config(page_title="LYZE | Aftermarket AI", layout="wide")

# Hide Streamlit default menu/footer
st.markdown("""
    <style>
        #MainMenu, footer {visibility: hidden;}
        .block-container { padding-top: 2rem; padding-bottom: 2rem; }
        .app-title {
            font-size: 28px;
            font-weight: 700;
            color: #1F2937;
            font-family: 'Segoe UI', sans-serif;
            padding-bottom: 0.5rem;
        }
        .description {
            color: #4B5563;
            font-size: 16px;
            margin-bottom: 2rem;
        }
        .module-card {
            background-color: #FFFFFF;
            border: 1px solid #E5E7EB;
            border-radius: 10px;
            padding: 1.5rem;
            height: 180px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            transition: 0.3s ease;
        }
        .module-card:hover {
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            background-color: #F9FAFB;
            cursor: pointer;
        }
        .module-icon {
            font-size: 28px;
            margin-bottom: 0.5rem;
        }
        .module-title {
            font-weight: 600;
            font-size: 18px;
            margin-bottom: 0.25rem;
            color: #111827;
        }
        .module-desc {
            font-size: 14px;
            color: #6B7280;
        }
        .upload-success {
            color: green;
            font-weight: 600;
            margin-top: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# ==== NAVIGATION ====
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

def navigate(page_name):
    st.session_state.current_page = page_name

# ==== HEADER ====
st.markdown('<div class="app-title">📊 LYZE - Aftermarket Intelligence</div>', unsafe_allow_html=True)
st.markdown('<div class="description">Upload Installed Base data and launch any module to begin analysis.</div>', unsafe_allow_html=True)

# ==== FILE UPLOAD (Updated for Multi-Industry Support) ====
uploaded_file = st.file_uploader("📁 Upload Installed Base CSV", type=["csv"], label_visibility="collapsed")
if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Define flexible core required columns for multi-industry use
    required_core = {"Equipment ID", "Location", "Usage Hours", "Service History", "Latitude", "Longitude", "ds"}
    expected_technical = {"Temperature", "Pressure", "Flow Rate", "RPM", "Voltage", "Current"}
    expected_categorical = {"Product Brand", "Application", "Market", "Product Code", "Equipment Type", "Industry"}

    all_expected = required_core.union(expected_technical).union(expected_categorical)
    missing = all_expected - set(df.columns)

    if required_core.issubset(df.columns):
        st.session_state["installed_base_data"] = df
        st.markdown('<div class="upload-success">✅ Data uploaded successfully.</div>', unsafe_allow_html=True)
        if missing:
            st.warning(f"⚠️ Some optional fields missing: {', '.join(missing)}. Analysis may be limited.")
    else:
        st.error(f"❌ Missing required core columns: {required_core - set(df.columns)}")
elif "installed_base_data" not in st.session_state:
    st.warning("⚠️ Upload a valid Installed Base CSV to proceed with module exploration.")





st.markdown("###")

# ==== MODULE GRID ====
row1_col1, row1_col2 = st.columns(2)
row2_col1, row2_col2 = st.columns(2)

with row1_col1:
    if st.button("📦 Installed Base", use_container_width=True):
        navigate("Installed Base")
    st.markdown("""
        <div class="module-card">
            <div class="module-icon">📦</div>
            <div class="module-title">Installed Base</div>
            <div class="module-desc">Map your equipment footprint and visualize usage, age, and location.</div>
        </div>
    """, unsafe_allow_html=True)

with row1_col2:
    if st.button("📈 Revenue Forecast", use_container_width=True):
        navigate("Revenue Forecast")
    st.markdown("""
        <div class="module-card">
            <div class="module-icon">📈</div>
            <div class="module-title">Revenue Forecast</div>
            <div class="module-desc">Time series predictions for aftermarket revenue planning.</div>
        </div>
    """, unsafe_allow_html=True)

with row2_col1:
    if st.button("⚙️ Parts Demand", use_container_width=True):
        navigate("Parts Demand")
    st.markdown("""
        <div class="module-card">
            <div class="module-icon">⚙️</div>
            <div class="module-title">Parts Demand</div>
            <div class="module-desc">Forecast part usage and optimize service part inventory.</div>
        </div>
    """, unsafe_allow_html=True)

with row2_col2:
    if st.button("💰 Opportunity Engine", use_container_width=True):
        navigate("Opportunity Engine")
    st.markdown("""
        <div class="module-card">
            <div class="module-icon">💰</div>
            <div class="module-title">Opportunity Engine</div>
            <div class="module-desc">Discover upsell, cross-sell, and retention opportunities.</div>
        </div>
    """, unsafe_allow_html=True)

st.write("---")
st.caption("© 2025 Aftermarket AI — All rights reserved.")

# ==== PAGE ROUTING ====
if st.session_state.current_page == "Installed Base":
    from modules.installed_base import render_installed_base
    render_installed_base()

elif st.session_state.current_page == "Revenue Forecast":
    from modules.forecasting import render_forecasting
    render_forecasting()

elif st.session_state.current_page == "Opportunity Engine":
    from modules.opportunity_engine import render_opportunities
    render_opportunities()

elif st.session_state.current_page == "Auth":
    from modules.auth import render_auth
    render_auth()
