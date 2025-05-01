import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from io import StringIO

# Helper function to display a download button
def download_csv(dataframe, filename="installed_base_data.csv"):
    csv = dataframe.to_csv(index=False)
    st.download_button(
        label="Download Data",
        data=csv,
        file_name=filename,
        mime="text/csv",
    )

def render_installed_base():
    # Back to Home button
    if st.button("🔙 Back to Home"):
        st.session_state.current_page = "Home"
        st.experimental_rerun()

    # Title and Instructions
    st.title("📦 Installed Base Intelligence")
    st.markdown(
        """
        Gain insights into your equipment base globally. Upload your data, analyze it interactively, and make data-driven decisions.
        Use the tools below to explore usage, service history, and other key metrics.
        """
    )

    # File Upload
    st.subheader("Upload Equipment Data")
    uploaded_file = st.file_uploader("Upload your equipment data (CSV)", type=["csv"])

    if uploaded_file is not None:
        # Read data and show basic details
        data = pd.read_csv(uploaded_file)
        st.write("### Raw Data Preview")
        st.dataframe(data.head(), use_container_width=True)

        # Check the structure of the file
        required_columns = ["Equipment ID", "Location", "Usage Hours", "Service History"]
        missing_columns = [col for col in required_columns if col not in data.columns]

        if missing_columns:
            st.error(f"Missing required columns: {', '.join(missing_columns)}")
        else:
            st.success("Data successfully loaded!")
            
            # Show basic statistics about the data
            st.write("### Data Overview")
            st.write(f"Total records: {data.shape[0]}")
            st.write(f"Total unique locations: {data['Location'].nunique()}")
            st.write(f"Average usage hours: {data['Usage Hours'].mean():,.2f}")
            
            # Visualizations
            st.write("### Equipment Distribution by Location")
            location_counts = data['Location'].value_counts()
            fig = px.bar(location_counts, x=location_counts.index, y=location_counts.values, labels={'x': 'Location', 'y': 'Count'})
            st.plotly_chart(fig, use_container_width=True)

            # Usage Hours Histogram
            st.write("### Distribution of Usage Hours")
            fig2 = px.histogram(data, x="Usage Hours", nbins=20, title="Usage Hours Distribution")
            st.plotly_chart(fig2, use_container_width=True)

            # Service History Breakdown
            st.write("### Service History Breakdown")
            service_counts = data['Service History'].value_counts()
            fig3 = px.pie(service_counts, names=service_counts.index, values=service_counts.values, title="Service History Distribution")
            st.plotly_chart(fig3, use_container_width=True)

            # Interactive Filtering by Location and Service History
            st.write("### Filter Data")
            location_filter = st.multiselect(
                "Select Locations", options=data['Location'].unique(), default=data['Location'].unique())
            service_filter = st.multiselect(
                "Select Service History Types", options=data['Service History'].unique(), default=data['Service History'].unique())

            # Filter the data based on the user input
            filtered_data = data[
                data['Location'].isin(location_filter) & data['Service History'].isin(service_filter)
            ]
            st.write(f"Filtered Data ({filtered_data.shape[0]} records)")
            st.dataframe(filtered_data, use_container_width=True)

            # Provide an option to download filtered data
            download_csv(filtered_data)

            # Summary Metrics for Filtered Data
            st.write("### Summary Metrics for Filtered Data")
            st.write(f"Total Units: {filtered_data.shape[0]}")
            st.write(f"Avg Usage Hours: {filtered_data['Usage Hours'].mean():,.2f}")
            st.write(f"Top Location: {filtered_data['Location'].value_counts().idxmax()}")
            st.write(f"Most Common Service History: {filtered_data['Service History'].value_counts().idxmax()}")
            
            # Optionally show a detailed breakdown
            st.write("### Detailed Breakdown of Equipment")
            st.dataframe(filtered_data, use_container_width=True)

            # Visualize a more detailed chart of usage by equipment
            st.write("### Equipment Usage Breakdown")
            usage_by_equipment = filtered_data.groupby("Equipment ID")["Usage Hours"].sum().reset_index()
            fig4 = px.bar(usage_by_equipment, x="Equipment ID", y="Usage Hours", title="Total Usage by Equipment")
            st.plotly_chart(fig4, use_container_width=True)
            
            st.success("Installed Base Analysis complete!")

