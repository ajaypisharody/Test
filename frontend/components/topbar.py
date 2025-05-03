import streamlit as st

def render_topbar():
    st.markdown("""
        <style>
            .top-bar {
                background-color: #FFFFFF;
                padding: 1rem 2rem;
                border-bottom: 1px solid #E0E0E0;
                display: flex;
                justify-content: space-between;
                align-items: center;
                box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            }
            .top-bar-title {
                font-size: 20px;
                font-weight: 600;
                color: #2C3E50;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            .top-bar-button {
                background-color: #0061F2;
                color: #FFFFFF;
                padding: 8px 16px;
                border: none;
                border-radius: 20px;
                font-weight: 500;
                cursor: pointer;
                transition: all 0.3s ease;
            }
            .top-bar-button:hover {
                background-color: #004bb5;
            }
        </style>
        <div class="top-bar">
            <div class="top-bar-title">LYZE Analytics Dashboard</div>
            <form action="">
                <button class="top-bar-button">🔐 Login / Signup</button>
            </form>
        </div>
    """, unsafe_allow_html=True)
