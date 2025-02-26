import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Load the dataset
file_path = "CAPSTONEDATA.csv"  # Ensure the correct file path

try:
    data = pd.read_csv(file_path)
    st.success("Data loaded successfully!")
except FileNotFoundError:
    st.error("File not found. Please upload the correct file.")
    st.stop()

# Display the first few rows of the dataset
st.write("### Preview of the dataset:")
st.dataframe(data)

# Ensure 'PROJDATE' is in datetime format
if 'PROJDATE' in data.columns:
    data['PROJDATE'] = pd.to_datetime(data['PROJDATE'], errors='coerce')

# Line chart of NETSALES over time
if 'PROJDATE' in data.columns and 'NETSALES' in data.columns:
    st.write("### NET SALES Trend Over Time")
    st.line_chart(data, x="PROJDATE", y="NETSALES")

# Scatter plot for NETSALES
st.write("### NET SALES Scatter Plot")
st.scatter_chart(data, x="PROJDATE", y="NETSALES")

# Histogram of Gross Sales using Matplotlib
if 'GROSSSALES' in data.columns:
    st.write("### Gross Sales Distribution")
    fig, ax = plt.subplots()
    ax.hist(data['GROSSSALES'], bins=20, color='skyblue', edgecolor='black')
    ax.set_xlabel("Gross Sales")
    ax.set_ylabel("Frequency")
    ax.set_title("Distribution of Gross Sales")
    st.pyplot(fig)  # Display the histogram

# Summary statistics
st.write("### Summary Statistics:")
st.write(data.describe())

# File uploader option for user to upload CSV
st.write("### Upload your CSV file")
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write("Uploaded Data:")
    st.dataframe(data)

st.divider()

import folium

from streamlit_folium import st_folium

# center on Liberty Bell, add marker
m = folium.Map(location=[39.949610, -75.150282], zoom_start=16)
folium.Marker(
    [39.949610, -75.150282], popup="Liberty Bell", tooltip="Liberty Bell"
).add_to(m)

# call to render Folium map in Streamlit
st_data = st_folium(m, width=725)

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim

# Load the dataset
file_path = "CAPSTONEDATA.csv"  # Ensure the correct file path

try:
    data = pd.read_csv(file_path)
    st.success("Data loaded successfully!")
except FileNotFoundError:
    st.error("File not found. Please upload the correct file.")
    st.stop()

# Display the first few rows of the dataset
st.write("### Preview of the dataset:")
st.dataframe(data)

# Ensure 'PROJDATE' is in datetime format
if 'PROJDATE' in data.columns:
    data['PROJDATE'] = pd.to_datetime(data['PROJDATE'], errors='coerce')

# Sales by Country
if 'COUNTRY' in data.columns and 'GROSSSALES' in data.columns:
    country_sales = data.groupby('COUNTRY')['GROSSSALES'].sum().reset_index()

    # Search for a country
    selected_country = st.selectbox("Search for a Country", ["All"] + list(country_sales['COUNTRY'].unique()))

    # Geolocation setup
    geolocator = Nominatim(user_agent="geoapi")


    def get_country_location(country):
        try:
            location = geolocator.geocode(country)
            if location:
                return (location.latitude, location.longitude)
        except:
            return None
        return None


    # Generate a Folium Map
    st.write("### Sales Map by Country")
    map_center = [20, 0]  # Default center
    m = folium.Map(location=map_center, zoom_start=2)

    for index, row in country_sales.iterrows():
        country = row["COUNTRY"]
        sales = row["GROSSSALES"]
        location = get_country_location(country)

        if location:
            color = "green" if sales > country_sales["GROSSSALES"].mean() else "red"
            folium.Marker(
                location,
                popup=f"{country}: ${sales:,.2f}",
                tooltip=f"{country} - {'High' if color == 'green' else 'Low'} Sales",
                icon=folium.Icon(color=color),
            ).add_to(m)

    # Zoom to selected country
    if selected_country != "All":
        selected_location = get_country_location(selected_country)
        if selected_location:
            m.location = selected_location
            m.zoom_start = 5

    st_folium(m, width=800, height=500)

