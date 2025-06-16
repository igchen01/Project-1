import streamlit as st
import plotly.express as px
import pandas as pd
import math
import folium
from shapely.geometry import Point, LineString, Polygon
from streamlit.components.v1 import html

# Load data
df = pd.read_csv("Airports_T.csv")

# Streamlit App Title
st.title("📊 Airports and Air Travel of US")

# Sidebar year slider
selected_year = st.sidebar.slider(
    "Select Year:",
    int(df["Year"].min()),
    int(df["Year"].max()),
    int(df["Year"].min()),
    step=4
)

# Filter by selected year
filtered_df = df[df["Year"] == selected_year]

if filtered_df.empty:
    st.warning(f"No data available for year {selected_year}")
    st.stop()

# Extract unique airports
airports = filtered_df[['Origin_airport', 'Org_airport_lat', 'Org_airport_long', 'Origin_population']].drop_duplicates(subset=['Origin_airport'])
airports.columns = ['Airport', 'Latitude', 'Longitude', 'Population']
airports = airports.dropna()

# Create folium map centered on the US
m = folium.Map(location=[39.8283, -98.5795], zoom_start=4)

# Add airports as circle markers
for _, row in airports.iterrows():
    folium.CircleMarker(
        location=[row["Latitude"], row["Longitude"]],
        radius=math.sqrt(math.sqrt(float(row["Population"])))/5,
        popup=f"Airport: {row['Airport']}<br>Population: {row['Population']}",
        color="blue",
        fill=True,
    ).add_to(m)

# Display map in Streamlit
map_html = m._repr_html_()
html(map_html, height=500, width=700)
