import streamlit as st
import pandas as pd
import plotly.express as px
import io

# Helper function to display a download button
def download_csv(dataframe, filename="installed_base_data.csv"):
    csv = dataframe.to_csv(index=False)
    st.download_button(
        label="Download Data as CSV",
        data=csv,
        file_name=filename,
        mime="text/csv",
    )

# Helper function for maintenance prediction
def predict_maintenance(data):
    threshold = 10000  # Maintenance threshold for usage hours
    data['Needs Maintenance'] = data['Usage Hours'] > threshold
    return data

# Helper function to convert data to Excel
def to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False)
    return output.getvalue()

# Function to display location heatmap (requires lat/lng data)
def location_heatmap(data):
    # Group the data by location and count occurrences
    location_counts = data['Location'].value_counts().reset_index()
    location_counts.columns = ['Location', 'Count']

    # Generate a heatmap
    fig = px.density_mapbox(
        location_counts, 
        lat="Latitude", lon="Longitude", 
        z="Count", radius=10, 
        center=dict(lat=37.77, lon=-122.42), 
        zoom=3,
        mapbox_style="carto-positron"
    )
    return fig

# Function to render historical trends (usage over time)
def render_usage_trends(data):
    if "ds" in data.columns and "Usage Hours" in data.columns:
        fig = px.line(data, x="ds", y="Usage Hours", title="Usage Hours Over Time")
        st.plotly_chart(fig)
    else:
        st.warning("No time-series data (ds) for usage hours available.")

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

    # File Upload with Tooltip
    st.subheader("Upload Equipment Data")
    st.markdown(
        """
        <style>
        .tooltip {
            position: relative;
        }
        .tooltip:hover:after {
            content: 'Please upload a CSV file containing equipment details like ID, location, and usage hours.';
            position: absolute;
            bottom: 30px;
            left: 10px;
            background-color: #333;
            color: white;
            padding: 5px;
            border-radius: 5px;
            font-size: 12px;
        }
        </style>
        """, unsafe_allow_html=True
    )
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
            
            # Predict Maintenance Needs
            data = predict_maintenance(data)

            # Maintenance Alert Dashboard
            st.write("### Maintenance Opportunity Dashboard")
            maintenance_data = data[data['Needs Maintenance']]
            if maintenance_data.empty:
                st.info("No equipment requires maintenance at this time.")
            else:
                st.warning(f"{maintenance_data.shape[0]} pieces of equipment require maintenance.")
                st.dataframe(maintenance_data[['Equipment ID', 'Usage Hours', 'Location', 'Service History', 'Needs Maintenance']], use_container_width=True)

            # Visualizations

            # Equipment Distribution by Location
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

            # Filter Data by Location and Service History
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
            
            # Render Historical Usage Trends (if data has time-series)
            render_usage_trends(filtered_data)

            # Provide an option to download filtered data as Excel
            download_excel(filtered_data)

            st.success("Installed Base Analysis complete!")
