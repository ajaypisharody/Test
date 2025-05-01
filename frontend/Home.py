import streamlit as st
from components.sidebar import render_sidebar

st.set_page_config(page_title="Aftermarket AI SaaS", layout="wide")
page = render_sidebar()

st.title("Aftermarket AI SaaS Platform")

if page == "🏠 Home":
    st.subheader("Overview Dashboard")
    st.write("Welcome to the Aftermarket AI platform. Use the sidebar to navigate.")
    st.markdown("""
    - 📦 Installed Base Intelligence
    - 📈 Revenue Forecasting
    - 💰 Opportunity Engine
    - ⚙️ Service Parts Demand Forecasting
    """)

elif page == "📦 Installed Base":
    from pages.installed_base import render_installed_base
    render_installed_base()

elif page == "📈 Revenue Forecast":
    from pages.forecasting import render_forecasting
    render_forecasting()

elif page == "💰 Opportunity Engine":
    from pages.opportunities import render_opportunities
    render_opportunities()

elif page == "⚙️ Parts Demand":
    from pages.parts_inventory import render_parts_inventory
    render_parts_inventory()

elif page == "🔐 Login/Signup":
    from pages.auth import render_auth
    render_auth()
