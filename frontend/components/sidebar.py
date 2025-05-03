import streamlit as st

def render_sidebar():
    with st.sidebar:
        st.markdown("### 🏢 LYZE AI Platform")
        st.markdown("Welcome to your aftermarket intelligence suite.")
        st.markdown("---")

        st.subheader("🔍 Navigation")
        st.page_link("Home.py", label="🏠 Dashboard Home")
        st.page_link("pages/installed_base.py", label="📦 Installed Base")
        st.page_link("pages/forecasting.py", label="📈 Revenue Forecast")
        st.page_link("pages/parts_inventory.py", label="⚙️ Parts Demand")
        st.page_link("pages/opportunity_engine.py", label="💰 Opportunity Engine")

        st.markdown("---")
        st.caption("© 2025 Aftermarket AI — All rights reserved.")
