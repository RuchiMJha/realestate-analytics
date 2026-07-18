import streamlit as st
import duckdb
import os
import pandas as pd

# Set up page layout
st.set_page_config(page_title="US Real Estate Analytics Hub", layout="wide")
st.title("🏡 US Real Estate Real-Time Analytics Hub")
st.markdown("This dashboard queries a local **2.1M+ row DuckDB database** dynamically based on your filters.")

DB_PATH = os.path.join("data", "processed", "real_estate.db")

# Establish connection to DuckDB
@st.cache_resource
def get_db_connection():
    return duckdb.connect(DB_PATH, read_only=True)

con = get_db_connection()

# --- SIDEBAR FILTERS ---
st.sidebar.header("Filter Options")

# Dynamic pull of states for the dropdown menu
states_list = [row[0] for row in con.execute("SELECT DISTINCT state FROM v_dashboard_properties WHERE state IS NOT NULL ORDER BY state").fetchall()]
selected_state = st.sidebar.selectbox("Select a State", states_list, index=states_list.index("California") if "California" in states_list else 0)

# Price range slider based on selected state data
min_max_price = con.execute(f"SELECT MIN(price), MAX(price) FROM v_dashboard_properties WHERE state = '{selected_state}'").fetchone()
min_p, max_p = float(min_max_price[0] or 0), float(min_max_price[1] or 1000000)

price_range = st.sidebar.slider(
    "Price Range ($)", 
    min_value=min_p, 
    max_value=max_p, 
    value=(min_p, max_p)
)

# --- QUERY THE DATABASE BASED ON FILTERS ---
query = """
    SELECT * 
    FROM v_dashboard_properties 
    WHERE state = ? 
      AND price BETWEEN ? AND ?
"""
df = con.execute(query, [selected_state, price_range[0], price_range[1]]).df()

# --- KEY PERFORMANCE METRICS (KPIs) ---
st.header(f"📊 Market Summary for {selected_state}")

kpi1, kpi2, kpi3 = st.columns(3)

with kpi1:
    st.metric(label="Total Active Listings", value=f"{len(df):,}")
with kpi2:
    avg_price = df['price'].mean() if not df.empty else 0
    st.metric(label="Average Listing Price", value=f"${avg_price:,.2f}")
with kpi3:
    avg_size = df['house_size'].mean() if not df.empty else 0
    st.metric(label="Avg House Size (Sq Ft)", value=f"{avg_size:,.0f} sq ft" if avg_size > 0 else "N/A")

st.markdown("---")

# --- DATA VISUALIZATION ---
st.subheader("Top Cities by Average Price in Selected Range")

if not df.empty:
    # Quick aggregation for visualization
    city_summary = df.groupby('city')['price'].mean().reset_index().sort_values(by='price', ascending=False).head(10)
    st.bar_chart(data=city_summary, x='city', y='price', use_container_width=True)
    
    # Raw Data Preview
    st.subheader("Raw Listings Explorer")
    st.dataframe(df.head(100), use_container_width=True)
else:
    st.warning("No listings found matching the selected criteria.")