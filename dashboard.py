import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
hour_data = pd.read_csv("hour_data.csv")
day_data = pd.read_csv("day_data.csv")

# Sidebar filters
st.sidebar.header("Filter Options")
view_dataset = st.sidebar.selectbox("Select Dataset", ["Hourly Data", "Daily Data"])
selected_year = st.sidebar.selectbox("Select Year", [2011, 2012])
selected_season = st.sidebar.multiselect("Select Season", [1, 2, 3, 4], default=[1, 2, 3, 4])
selected_weathersit = st.sidebar.multiselect("Select Weather Situation", [1, 2, 3, 4], default=[1, 2, 3, 4])

# Filter data based on selection
if view_dataset == "Hourly Data":
    data = hour_data
else:
    data = day_data

data = data[(data['yr'] == (selected_year - 2011)) & (data['season'].isin(selected_season)) & (data['weathersit'].isin(selected_weathersit))]

# Title and description
st.title("Bike Rental Dashboard")
st.write("Explore bike rental data using filters and visualizations.")

# Visualizations
st.subheader(f"Bike Rentals ({view_dataset})")

# Total rentals
total_rentals = data['cnt'].sum()
st.metric(label="Total Rentals", value=total_rentals)

# Rentals by season
season_rentals = data.groupby('season')['cnt'].sum().reset_index()
season_names = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
season_rentals['season'] = season_rentals['season'].map(season_names)

fig, ax = plt.subplots()
ax.bar(season_rentals['season'], season_rentals['cnt'], color='skyblue')
ax.set_title("Total Rentals by Season")
ax.set_xlabel("Season")
ax.set_ylabel("Rentals")
st.pyplot(fig)

# Rentals by weather situation
weather_rentals = data.groupby('weathersit')['cnt'].sum().reset_index()
weather_names = {
    1: "Clear/Partly Cloudy",
    2: "Mist/Cloudy",
    3: "Light Snow/Rain",
    4: "Heavy Rain/Snow"
}
weather_rentals['weathersit'] = weather_rentals['weathersit'].map(weather_names)

fig, ax = plt.subplots()
ax.pie(weather_rentals['cnt'], labels=weather_rentals['weathersit'], autopct='%1.1f%%', startangle=140, colors=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99'])
ax.set_title("Rentals by Weather Situation")
st.pyplot(fig)

# Time-based trends
if 'hr' in data.columns:
    hourly_data = data.groupby('hr')['cnt'].mean().reset_index()
    fig, ax = plt.subplots()
    ax.plot(hourly_data['hr'], hourly_data['cnt'], marker='o', color='green')
    ax.set_title("Average Rentals by Hour")
    ax.set_xlabel("Hour")
    ax.set_ylabel("Average Rentals")
    st.pyplot(fig)
