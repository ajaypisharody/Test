import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import io


def render_opportunities():
    st.title("💰 Opportunity Engine")
    st.markdown("""
    Identify new revenue opportunities by correlating internal Installed Base data with macroeconomic indicators and industry trends.
    This model applies a scoring framework inspired by strategic consulting firms.
    """)

    # Simulated Installed Base Data
    installed_base = pd.DataFrame({
        "Customer": ["Acme Corp", "Beta Inc", "Nova Systems", "Zeta Ltd"],
        "Country": ["USA", "Germany", "India", "Brazil"],
        "Product": ["Compressor", "Valve", "Compressor", "Pump"],
        "Units Installed": [100, 50, 80, 40],
        "Avg Usage Hours": [12000, 8000, 14000, 9000],
        "Last Purchase Year": [2020, 2019, 2021, 2020]
    })

    # Simulated Product Profitability
    product_profit = pd.DataFrame({
        "Product": ["Compressor", "Valve", "Pump"],
        "Gross Margin %": [42, 35, 38],
        "Replacement Cycle (yrs)": [5, 7, 6]
    })

    # Simulated Country Indicators
    country_indicators = pd.DataFrame({
        "Country": ["USA", "Germany", "India", "Brazil"],
        "GDP Growth %": [2.1, 1.2, 6.3, 2.8],
        "Inflation %": [3.0, 2.5, 5.5, 4.2],
        "Market Index Growth %": [5.2, 3.1, 8.4, 4.7],
        "Competitive Intensity": ["High", "Medium", "Low", "Medium"]
    })

    # Merge data for scoring
    df = installed_base.merge(product_profit, on="Product", how="left")
    df = df.merge(country_indicators, on="Country", how="left")

    # Scoring logic
    def score_opportunity(row):
        score = 0
        score += min(row["Units Installed"] / 20, 5)
        score += (2025 - row["Last Purchase Year"]) * 0.5
        score += row["Gross Margin %"] / 10
        score += row["GDP Growth %"] / 2
        score += row["Market Index Growth %"] / 2
        if row["Competitive Intensity"] == "High":
            score -= 2
        elif row["Competitive Intensity"] == "Medium":
            score -= 1
        return round(score, 2)

    df["Opportunity Score"] = df.apply(score_opportunity, axis=1)
    df = df.sort_values(by="Opportunity Score", ascending=False)

    # Filters
    with st.sidebar:
        st.header("🔍 Filters")
        selected_country = st.multiselect("Select Country", df["Country"].unique(), default=df["Country"].unique())
        selected_product = st.multiselect("Select Product", df["Product"].unique(), default=df["Product"].unique())

    filtered_df = df[(df["Country"].isin(selected_country)) & (df["Product"].isin(selected_product))]

    st.subheader("🔍 Opportunity Insights")
    st.dataframe(filtered_df[[
        "Customer", "Country", "Product", "Units Installed", 
        "Avg Usage Hours", "Last Purchase Year", 
        "Gross Margin %", "GDP Growth %", "Market Index Growth %",
        "Competitive Intensity", "Opportunity Score"
    ]], use_container_width=True)

    st.subheader("📊 Opportunity Score by Customer")
    fig = px.bar(filtered_df, x="Customer", y="Opportunity Score", color="Product", text="Country")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🌎 Opportunity Score by Country")
    fig2 = px.scatter_geo(filtered_df, locations="Country", locationmode="country names",
                          size="Opportunity Score", color="Product",
                          projection="natural earth", title="Geographic Opportunity Heatmap")
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("📈 Correlation Matrix")
    numeric_df = filtered_df.select_dtypes(include=["float64", "int"])
    corr = numeric_df.corr()
    fig3 = px.imshow(corr, text_auto=True, title="Correlation Between Key Drivers")
    st.plotly_chart(fig3, use_container_width=True)

    # Download button
    csv = filtered_df.to_csv(index=False)
    st.download_button("📥 Download Opportunities as CSV", csv, "opportunity_insights.csv", "text/csv")

    st.success("Opportunity analysis completed with embedded datasets and strategic scoring.")
