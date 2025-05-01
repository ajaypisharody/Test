import streamlit as st
import pandas as pd

def render_installed_base():
    # Back to Home button
    if st.button("🔙 Back to Home"):
        st.session_state.current_page = "Home"
        st.experimental_rerun()

    st.title("📦 Installed Base Intelligence")
    st.markdown("Gain insights into your global equipment base, including usage, location, and service history.")

    # Simulated Installed Base Data
    data = pd.DataFrame({
        "Equipment ID": [101, 102, 103, 104],
        "Location": ["New York", "Berlin", "Tokyo", "Mumbai"],
        "Usage Hours": [5200, 11000, 8700, 7600],
        "Service History": ["Regular", "Heavy", "Moderate", "Light"]
    })

    # High-level metrics
    st.write("")
    col1, col2, col3 = st.columns(3)

    col1.metric("Total Units", f"{data.shape[0]}")
    col2.metric("Avg Usage Hours", f"{int(data['Usage Hours'].mean())}")
    col3.metric("Top Region", data["Location"].value_counts().idxmax())

    st.write("")
    st.markdown("### Equipment Overview")
    st.dataframe(data, use_container_width=True)
    st.success("Installed base data loaded successfully.")
