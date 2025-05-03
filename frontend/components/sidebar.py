import streamlit as st

def render_sidebar(navigate):
    with st.sidebar:
        st.image("assets/logo.png", use_column_width=True)
        st.markdown("---")
        st.markdown("**LYZE AI Analytics Suite**")
        
        if st.button("🏠 Home"):
            navigate("Home")
        if st.button("📦 Installed Base"):
            navigate("Installed Base")
        if st.button("📈 Revenue Forecast"):
            navigate("Revenue Forecast")
        if st.button("⚙️ Parts Demand"):
            navigate("Parts Demand")
        if st.button("💰 Opportunity Engine"):
            navigate("Opportunity Engine")
