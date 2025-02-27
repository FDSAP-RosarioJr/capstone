import streamlit as st

st.title("My Capstone Test Project")
st.subheader("Welcome to My Capstone Test Project")
st.write("Join us and learn more knowledge about the My Capstone Project.!")
st.divider()
st.image("capstone.gif", "Start Your Capstone Project.!")
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

st.divider()

st.image("capstone.png", "Lets start our Journey in Capstone Project.!")
st.divider()
st.image("new pic.png", "Lets start our Journey in Capstone Project.!")