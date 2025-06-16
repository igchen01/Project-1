import streamlit as st
import plotly.express as px
import pandas as pd
import math
import folium
from shapely.geometry import Point, LineString, Polygon


df = pd.read_csv("Airports_T.csv")
df['Year'] = pd.to_datetime(df['Fly_date']).dt.year

# Streamlit App Title
st.title("📊 Airports and Air Travel of US")

# Create a sidebar filter for selecting a year
selected_year = st.sidebar.slider("Select Year:", int(df["Year"].min()), int(df["Year"].max()), int(df["Year"].min()), step = 4)

# Filter data based on the selected year
filtered_df = df[df.year == selected_year]

#Find all the airports
airports = filtered_df[['Origin_airport', 'Org_airport_lat', 'Org_airport_long','Origin_population']].drop_duplicates(subset=['Origin_airport'])
airports.columns = ['Airport', 'Latitude', 'Longitude','Population']
airports = airports.dropna()


m = folium.Map(location=[20,0], zoom_start=2)

#Mapping the location of airports

for _, row in airports.iterrows():
    folium.CircleMarker(
        location=[row["Latitude"], row["Longitude"]],
        radius=math.sqrt(math.sqrt(float(row["Population"])))/5,
        popup=f"Airport:{row['Airport']}<br>Population:{row['Population']}",
        color="blue",
        fill=True,
    ).add_to(m)

from folium import Map
from streamlit.components.v1 import html

map_html = m._repr_html_()
html(map_html, height=500, width=700)
