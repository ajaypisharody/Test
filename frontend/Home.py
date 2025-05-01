import streamlit as st
import sys, os

# Path setup to allow imports from parent and sibling folders
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from components.sidebar import render_sidebar

st.set_page_config(page_title="Lyze | Dashboard", layout="wide")

# Load sidebar and current page selection
page = render_sidebar()

st.markdown(
    """
    <style>
        .big-font { font-size:36px !important; font-weight: bold; }
        .metric-card {
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 1.5rem;
            text-align: center;
            background-color: #f9f9f9;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Home Dashboard View
if page == "🏠 Home":
    st.markdown('<div class="big-font">📊 AI SaaS Dashboard</div>', unsafe_allow_html=True)
    st.markdown("Welcome to your analytics control center. Navigate using the sidebar to explore specific modules.")

    st.write("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="metric-card">
                <h4>📦 Installed Base</h4>
                <p>View your global equipment footprint, lifecycle usage, and service records.</p>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown(
            """
            <div class="metric-card">
                <h4>📈 Revenue Forecast</h4>
                <p>AI-based revenue predictions using historical trends and time series modeling.</p>
            </div>
            """, unsafe_allow_html=True)

    with col3:
        st.markdown(
            """
            <div class="metric-card">
                <h4>⚙️ Parts Demand</h4>
                <p>Forecast parts requirements based on machine usage patterns and service needs.</p>
            </div>
            """, unsafe_allow_html=True)

    st.write("")
    col4, col5 = st.columns(2)

    with col4:
        st.markdown(
            """
            <div class="metric-card">
                <h4>💰 Opportunity Engine</h4>
                <p>Detect churn risks and upsell opportunities using smart segmentation.</p>
            </div>
            """, unsafe_allow_html=True)

    with col5:
        st.markdown(
            """
            <div class="metric-card">
                <h4>🔐 User Login</h4>
                <p>Enterprise-ready authentication for secure access and user control.</p>
            </div>
            """, unsafe_allow_html=True)

    st.write("---")
    st.caption("© 2025 Insiful AI — All rights reserved.")

# Route to other pages
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
