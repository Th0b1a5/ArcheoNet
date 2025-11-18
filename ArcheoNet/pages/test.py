import streamlit as st
import folium
from streamlit_folium import st_folium
from datetime import datetime

try:
	username = (st.session_state['userID'])
except:
	st.switch_page(r"database\login.py")
if st.session_state["userID"] == None or st.session_state["userID"] == "":
	st.switch_page("login.py")
      
if "last_object" not in st.session_state:
    st.session_state['last_object'] = None

# Sample marker data
locations = [
    {"name": "Place A", "lat": 40.7128, "lon": -74.0060, "info": "Info about Place A", "tag": "A ID"},
    {"name": "Place B", "lat": 34.0522, "lon": -118.2437, "info": "Info about Place B", "tag": "B ID"},
    {"name": "Place C", "lat": 37.7749, "lon": -122.4194, "info": "Info about Place C", "tag": "C ID"}
]

# Initialize the map at the average location
avg_lat = sum(loc["lat"] for loc in locations) / len(locations)
avg_lon = sum(loc["lon"] for loc in locations) / len(locations)
m = folium.Map(location=[avg_lat, avg_lon], zoom_start=4)

# Add markers with popups
for loc in locations:
    folium.Marker(
        [loc["lat"], loc["lon"]],
        tooltip=loc["name"],
        popup=loc["info"]
    ).add_to(m)

# Display map in Streamlit and capture clicks
map_data = st_folium(m, width=700, height=450)

# Check if user clicked somewhere on the map
if map_data and map_data.get("last_object_clicked"):

    clicked_lat = map_data["last_object_clicked"]["lat"]
    clicked_lon = map_data["last_object_clicked"]["lng"]
    
    object_name = map_data["last_object_clicked_tooltip"]

    if object_name != st.session_state['last_object']:
        st.session_state['last_object'] = object_name
        print(f"{datetime.now():%Y-%m-%d %H:%M:%S} on {object_name} at Lat: {clicked_lat}, Lon: {clicked_lon}")
        
    else:
        pass