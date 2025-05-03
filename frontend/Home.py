import streamlit as st
import pandas as pd
import sys, os

# Path setup
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Streamlit config
st.set_page_config(page_title="LYZE | Analytics", layout="wide")

# Component Imports
from components.sidebar import render_sidebar
from components.topbar import render_topbar

# State Setup
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

def navigate(page_name):
    st.session_state.current_page = page_name

# ===== Styling =====
st.markdown("""
    <style>
        #MainMenu, footer {visibility: hidden;}
        .app-header {
            font-size: 28px;
            font-weight: 600;
            color: #1F2937;
            margin-bottom: 1rem;
            font-family: 'Segoe UI', sans-serif;
        }
        .card-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1.25rem;
            margin-top: 1rem;
        }
        .card {
            background: #F9FAFB;
            border: 1px solid #E5E7EB;
            border-radius: 12px;
            padding: 1rem 1.25rem;
            transition: all 0.2s ease;
            height: 140px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        .card:hover {
            background-color: #F3F4F6;
            box-shadow: 0 4px 12px rgba(0,0,0,0.06);
            cursor: pointer;
        }
        .card-title {
            font-weight: 600;
            font-size: 16px;
            color: #111827;
        }
        .card-desc {
            font-size: 14px;
            color: #6B7280;
        }
    </style>
""", unsafe_allow_html=True)

# ===== Layout =====
render_topbar()
render_sidebar(navigate)

if st.session_state.current_page == "Home":

    st.markdown('<div class="app-header">LYZE - AI Analytics</div>', unsafe_allow_html=True)
    st.write("Upload Installed Base data to begin.")

    uploaded_file = st.file_uploader("Upload Installed Base CSV", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        required = {"Equipment ID", "Location", "Usage Hours", "Service History", "Latitude", "Longitude", "ds"}
        if required.issubset(df.columns):
            st.session_state["installed_base_data"] = df
            st.success("✅ File uploaded successfully.")
            st.dataframe(df.head())
        else:
            st.error(f"❌ Missing required columns: {required - set(df.columns)}")
    elif "installed_base_data" not in st.session_state:
        st.warning("⚠️ Please upload a valid CSV file to use the modules.")

    # ===== Cards =====
    st.markdown('<div class="card-grid">', unsafe_allow_html=True)

    # Installed Base
    st.markdown(f"""
        <div class="card" onclick="window.location.href='#{navigate("Installed Base")}'">
            <div class="card-title">📦 Installed Base</div>
            <div class="card-desc">View equipment footprint and service data.</div>
        </div>
    """, unsafe_allow_html=True)

    # Revenue Forecast
    st.markdown(f"""
        <div class="card" onclick="window.location.href='#{navigate("Revenue Forecast")}'">
            <div class="card-title">📈 Revenue Forecast</div>
            <div class="card-desc">Time series forecast for revenue planning.</div>
        </div>
    """, unsafe_allow_html=True)

    # Parts Demand
    st.markdown(f"""
        <div class="card" onclick="window.location.href='#{navigate("Parts Demand")}'">
            <div class="card-title">⚙️ Parts Demand</div>
            <div class="card-desc">Predict part consumption based on installed base.</div>
        </div>
    """, unsafe_allow_html=True)

    # Opportunity Engine
    st.markdown(f"""
        <div class="card" onclick="window.location.href='#{navigate("Opportunity Engine")}'">
            <div class="card-title">💰 Opportunity Engine</div>
            <div class="card-desc">Identify upsell, cross-sell and churn risk signals.</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.write("---")
    st.caption("© 2025 Aftermarket AI — All rights reserved.")

# ========== Page Routing (manual) ==========
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
