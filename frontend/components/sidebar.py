import streamlit as st
import os

def render_sidebar():
    logo_path = "frontend/assets/images/logo.png"
    
    if os.path.exists(logo_path):
        st.sidebar.image(logo_path, use_column_width=True)
    else:
        st.sidebar.markdown("### Aftermarket AI")

    st.sidebar.title("Navigation")
    return st.sidebar.radio("Go to", [
        "🏠 Home",
        "📦 Installed Base",
        "📈 Revenue Forecast",
        "💰 Opportunity Engine",
        "⚙️ Parts Demand",
        "🔐 Login/Signup"
    ])
