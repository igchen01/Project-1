import pandas as pd
import plotly.express as px
import folium
import numpy as np
import math
import calendar
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import matplotlib.pyplot as plt
from shapely.geometry import Point, LineString, Polygon
import streamlit as st


#Title of the app
st.title("Airline A Dashboard")
st.write("Analysis of Airline A data to determine potential upgrade of existing fleet")

#Data reading

df = pd.read_csv("Airports_P.csv")
dt = pd.read_csv("Airports_T.csv")
#dd = pd.read_csv("Airports_D.csv")


monthly_flights = dt.groupby('Fly_date')['Flights'].sum().reset_index()
monthly_flights['Fly_date'] = pd.to_datetime(monthly_flights['Fly_date'])
monthly_flights = monthly_flights.sort_values(by='Fly_date')
monthly_flights['Rolling_Avg'] = monthly_flights['Flights'].rolling(window=3).mean()

#Create a second line chart
fig2 = px.line(
    monthly_flights,
    x='Fly_date',
    y=['Flights', 'Rolling_Avg'],
    labels={'Fly_date': 'Year', 'Flights': 'Number of Flights'},
    color_discrete_map={
        'Flights': 'blue',
        'Rolling_Avg': 'green'
    }
)

#Forcasting the time series for number of flights

monthly_flights = dt.groupby('Fly_date')['Flights'].sum().reset_index()
monthly_flights['Fly_date'] = pd.to_datetime(monthly_flights['Fly_date'])
monthly_flights = monthly_flights.sort_values(by='Fly_date')
monthly_flights.set_index('Fly_date', inplace=True)

model = ExponentialSmoothing(monthly_flights['Flights'],
                              trend='mul',
                              seasonal='mul',
                              damped_trend=True,
                              seasonal_periods=12,
                              initialization_method='estimated')


fit = model.fit()
forecast = fit.forecast(24)

plt.figure(figsize=(10, 5))
plt.plot(monthly_flights['Flights'], label='Observed')
plt.plot(forecast.index, forecast, label='Forecast', linestyle='--')
plt.legend()
plt.xlabel('Year')
plt.ylabel('Number of Flights')
plt.title('Holt-Winters Forecast')
plt.show()

# Display the plots in Streamlit
st.subheader("Airline A Monthly Flights with Rolling Average (3 months)")
st.plotly_chart(fig2)
st.subheader("Airline A Flights Forecast")
st.pyplot(plt)
plt.clf()

# ----------------- Forecasting Passengers ------------------
# Preprocess the data for monthly passengers
monthly_passengers = dt.groupby('Fly_date')['Passengers'].sum().reset_index()
monthly_passengers['Fly_date'] = pd.to_datetime(monthly_passengers['Fly_date'])
monthly_passengers = monthly_passengers.sort_values(by='Fly_date')
monthly_passengers.set_index('Fly_date', inplace=True)

# Fit the Holt-Winters Exponential Smoothing Model for Passengers (multiplicative trend and seasonality)
model_passengers = ExponentialSmoothing(monthly_passengers['Passengers'],
                                         trend='mul',
                                         seasonal='mul',
                                         damped_trend=True,
                                         seasonal_periods=12,
                                         initialization_method='estimated')

fit_passengers = model_passengers.fit()
forecast_passengers = fit_passengers.forecast(24)

# Plot for Passengers Forecast
plt.figure(figsize=(10, 5))
plt.plot(monthly_passengers['Passengers'], label='Observed (Passengers)', color='blue')
plt.plot(forecast_passengers.index, forecast_passengers, label='Forecast (Passengers)', linestyle='--', color='green')
plt.legend(loc='lower right')
plt.xlabel('Year')
plt.ylabel('Number of Passengers')
plt.title('Holt-Winters Forecast for Passengers')

# Display the plots in Streamlit
st.subheader("Airline A Monthly Passengers with Rolling Average (3 months)")
st.subheader("Airline A Passenger Forecast")
st.pyplot(plt)
plt.clf()

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

map_html = m._repr_html_()
components.html(map_html, height=500, width=700)
html(map_html, height=500, width=700)
