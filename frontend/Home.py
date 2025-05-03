import streamlit as st
import pandas as pd
import sys, os

# Path setup
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from components.sidebar import render_sidebar
from components.topbar import render_topbar

st.set_page_config(page_title="LYZE Analytics", layout="wide")

# Hide Streamlit UI elements
st.markdown("""
    <style>
        #MainMenu, footer {visibility: hidden;}
        .block-container { padding: 1rem 2rem; }
        .app-header {
            font-size: 28px;
            font-weight: 600;
            margin-bottom: 1rem;
            font-family: 'Segoe UI', sans-serif;
        }
        .tile-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
            margin-top: 2rem;
        }
        .tile {
            background: #F9FAFB;
            border: 1px solid #E5E7EB;
            border-radius: 12px;
            padding: 1.5rem;
            transition: 0.2s ease;
            box-shadow: 0 1px 3px rgba(0,0,0,0.06);
        }
        .tile:hover {
            background-color: #F3F4F6;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            cursor: pointer;
        }
        .tile-title {
            font-size: 20px;
            font-weight: 600;
            margin-bottom: 0.5rem;
            color: #1F2937;
        }
        .tile-desc {
            font-size: 14px;
            color: #4B5563;
        }
    </style>
""", unsafe_allow_html=True)

if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

def navigate(page_name):
    st.session_state.current_page = page_name
    st.rerun()

# Render
render_topbar()
render_sidebar(navigate)

if st.session_state.current_page == "Home":
    st.markdown('<div class="app-header">📊 LYZE - AI Analytics</div>', unsafe_allow_html=True)
    st.write("Welcome to your enterprise analytics suite. Upload data and click a module to get started.")

    st.subheader("📁 Upload Installed Base CSV")
    uploaded_file = st.file_uploader("Upload CSV with columns like `Equipment ID`, `Location`, `Usage Hours`, etc.", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        required = {"Equipment ID", "Location", "Usage Hours", "Service History", "Latitude", "Longitude", "ds"}
        if required.issubset(df.columns):
            st.session_state["installed_base_data"] = df
            st.success("✅ Data uploaded. All modules can now access it.")
            st.dataframe(df.head())
        else:
            st.error(f"❌ Missing required columns: {required - set(df.columns)}")
    elif "installed_base_data" not in st.session_state:
        st.warning("⚠️ Please upload a valid CSV to proceed.")

    # ==== Modules Grid ====
    st.markdown('<div class="tile-grid">', unsafe_allow_html=True)

    st.markdown(f"""
        <div class="tile" onclick="window.location.href='#{navigate('Installed Base')}';">
            <div class="tile-title">📦 Installed Base</div>
            <div class="tile-desc">View equipment footprint and service data.</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="tile" onclick="window.location.href='#{navigate('Revenue Forecast')}';">
            <div class="tile-title">📈 Revenue Forecast</div>
            <div class="tile-desc">Time series forecast for revenue planning.</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="tile" onclick="window.location.href='#{navigate('Parts Demand')}';">
            <div class="tile-title">⚙️ Parts Demand</div>
            <div class="tile-desc">Predict service part consumption intelligently.</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="tile" onclick="window.location.href='#{navigate('Opportunity Engine')}';">
            <div class="tile-title">💰 Opportunity Engine</div>
            <div class="tile-desc">Identify churn risks and upsell opportunities.</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    st.write("---")
    st.caption("© 2025 Aftermarket AI — All rights reserved.")

# Page Routing
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
