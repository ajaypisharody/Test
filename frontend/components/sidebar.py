import streamlit as st

def render_sidebar():
    st.sidebar.image("assets/images/logo.png", use_column_width=True)
    st.sidebar.title("Navigation")
    return st.sidebar.radio("Go to", [
        "🏠 Home",
        "📦 Installed Base",
        "📈 Revenue Forecast",
        "💰 Opportunity Engine",
        "⚙️ Parts Demand",
        "🔐 Login/Signup"
    ])
