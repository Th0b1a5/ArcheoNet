import streamlit as st
from streamlit_geolocation import streamlit_geolocation
from streamlit_js_eval import streamlit_js_eval, copy_to_clipboard, create_share_link, get_geolocation
import pandas as pd
import numpy as np
from streamlit.runtime import get_instance
from datetime import datetime
from pathlib import Path
import pydeck as pdk
import sqlite3
import time
import socket
import secrets
import re
import folium
from streamlit_folium import st_folium
from PIL import Image, ImageOps
import io

import modules.get_ip as get_ip
import modules.location as location
import modules.styles as styles

st.session_state.page = Path(__file__).name.replace('.py', '')
print(f"Device connected! {datetime.now():%Y-%m-%d %H:%M:%S} - IP: {get_ip.pull_ip()} - {st.session_state.page}")

try:
	username = (st.session_state['userID'])
except:
	st.switch_page("login.py")
if st.session_state["userID"] == None or st.session_state["userID"] == "":
	st.switch_page("login.py")
	
if "last_object" not in st.session_state:
    st.session_state['last_object'] = None

user_lat, user_lon = location.get_geolocation()
st.write(user_lat, user_lon)


# Sample marker data
locations = [
    {"name": "You", "lat": user_lat, "lon": user_lon, "info": "user", "tag": "user"}
]

# Initialize the map at the average location
m = folium.Map(location=[user_lat, user_lon], zoom_start=4)

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
if map_data:
    print(map_data)

if map_data and map_data.get("last_object_clicked"):
    clicked_identifier = map_data.get("last_object_clicked")
    print(clicked_identifier)
    
    if clicked_identifier == "user":
        print("Clicked on user")

    else:
        clicked_lat = map_data["last_object_clicked"]["lat"]
        clicked_lon = map_data["last_object_clicked"]["lng"]
        
        object_name = map_data["last_object_clicked_tooltip"]

        if object_name != st.session_state['last_object']:
            st.session_state['last_object'] = object_name
            print(f"{datetime.now():%Y-%m-%d %H:%M:%S} on {object_name} at Lat: {clicked_lat}, Lon: {clicked_lon}")
            
        else:
            pass