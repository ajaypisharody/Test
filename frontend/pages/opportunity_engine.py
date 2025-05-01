import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Opportunity Engine", layout="wide")
st.title("💰 Opportunity Engine - Strategic Growth Insights")

st.markdown("""
This module uses your installed base data, customer profiles, product intelligence,
and economic indicators to generate statistically scored growth opportunities.
""")

# 1. Static Installed Base Data
installed_base = pd.DataFrame({
    'Customer': ['Alpha Corp', 'Beta Inc', 'Gamma Ltd', 'Delta Co'],
    'Country': ['USA', 'Germany', 'India', 'Brazil'],
    'Product': ['X100', 'X200', 'X100', 'X300'],
    'Units': [120, 85, 150, 60],
    'Average Usage Hours': [10500, 8700, 9400, 11000],
    'Sales History': [2, 1, 3, 2],
    'Lifecycle Stage': ['Growth', 'Mature', 'Growth', 'Decline']
})

# 2. Static GDP & Market Index Proxy Data
economic_indicators = pd.DataFrame({
    'Country': ['USA', 'Germany', 'India', 'Brazil'],
    'GDP Growth (%)': [2.5, 1.8, 6.3, 2.1],
    'Market Momentum Index': [0.7, 0.6, 0.9, 0.5]
})

# 3. Join data sets
merged = installed_base.merge(economic_indicators, on='Country', how='left')

# 4. Scoring System: 0-1 scale weighted by strategic importance
def score_opportunity(row):
    lifecycle_score = {'Growth': 1.0, 'Mature': 0.5, 'Decline': 0.2}.get(row['Lifecycle Stage'], 0.3)
    normalized_units = row['Units'] / 150  # Assume 150 is max
    normalized_usage = row['Average Usage Hours'] / 12000  # Assume 12k is upper threshold
    normalized_gdp = row['GDP Growth (%)'] / 10  # Normalize GDP
    momentum = row['Market Momentum Index']
    sales_boost = 0.1 * row['Sales History']

    score = (
        0.2 * normalized_units +
        0.2 * normalized_usage +
        0.25 * normalized_gdp +
        0.15 * momentum +
        0.1 * lifecycle_score +
        0.1 * sales_boost
    )
    return round(score, 3)

merged['Opportunity Score'] = merged.apply(score_opportunity, axis=1)

# 5. Display Table
st.subheader("📋 Opportunity Scorecard")
st.dataframe(merged[['Customer', 'Country', 'Product', 'Opportunity Score']], use_container_width=True)

# 6. Visualizations
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 📈 Scores by Country")
    fig1 = px.bar(merged, x='Country', y='Opportunity Score', color='Opportunity Score',
                 color_continuous_scale='Viridis', title="Opportunity Scores Across Countries")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown("#### 🔍 Opportunity by Product")
    fig2 = px.sunburst(merged, path=['Country', 'Product', 'Customer'], values='Opportunity Score',
                       title="Opportunity Breakdown by Product")
    st.plotly_chart(fig2, use_container_width=True)

# 7. Top Recommendations
st.subheader("🚀 High-Scoring Growth Opportunities")
top_opportunities = merged.sort_values("Opportunity Score", ascending=False).head(3)
st.table(top_opportunities[['Customer', 'Country', 'Product', 'Opportunity Score']])

st.success("Analysis complete. Insights ready for business decision-making.")
