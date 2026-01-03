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

# =======INITALIZE SESSION STATE VARIABLES AND OTHER =======
try:
	userID = (st.session_state['userID'])
	username = (st.session_state['username'])
except:
	st.switch_page(r"login.py")
if st.session_state["userID"] == None or st.session_state["userID"] == "":
	st.switch_page("login.py")
	
if "last_id" not in st.session_state:
    st.session_state['last_id'] = None

if "locations" not in st.session_state:
    st.session_state['locations'] = []


# Initialize session state for toggle
if "display_window" not in st.session_state:
    st.session_state.display_window = False



def toggle_display_window():
    st.session_state.display_window = not st.session_state.display_window

fullscreen_map_css = """
<style>
/* Hide the Streamlit header and footer */
[data-testid="stHeader"], footer {
    display: none;
}

/* Remove all margins and padding from the main page */
.block-container {
    padding-top: 0rem !important;
    padding-bottom: 0rem !important;
    padding-left: 0rem !important;
    padding-right: 0rem !important;
    max-width: 100% !important;
}

iframe[title="streamlit_folium.st_folium"] {
    position: fixed !important;
    top: 0 !important;        /* Kills the black bar at the top */
    left: 0 !important;
    width: 100vw !important;
    height: 100vh !important;
    z-index: 1 !important;    /* Keeps it in the background */
    border: none !important;
}
"""
st.markdown(fullscreen_map_css, unsafe_allow_html=True)


display_window_css = """
<style>
@keyframes slideUp {
  from { transform: translateY(100%); }
  to { transform: translateY(0); }
}

@keyframes buttonSlide {
  from { transform: translateY(65vh); opacity: 0; } 
  to { transform: translateY(0); opacity: 1; }
}

#display_window {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    height: 65vh; 
    background-color: #262730;
    border-top: 5px solid #666;
    box-shadow: 0 -2px 10px rgba(0,0,0,0.3);
    overflow: auto;
    transition: transform 0.4s ease-in-out;
    transform: translateY(100%);
    z-index: 9999;
    padding: 30px;
}
#display_window.open {
    animation: slideUp 0.4s ease-out forwards;
}

button.inner-btn {
    margin: 5px;
    padding: 8px 15px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
}

button.inner-btn:hover {
    background-color: #0056b3;
    cursor: pointer;
}

div.stButton > button[kind="primary"] {
    position: fixed;
    bottom: 56vh;
    right: 22px;
    z-index: 10000;
    width: 40px;
    height: 40px;
    font-size: 28px !important;
    line-height: 1 !important; /* Helps keep it centered vertically */
    padding: 0 !important;
    margin: 0 !important;

    animation: buttonSlide 0.4s ease-out forwards;
}

</style>
"""



# Embed the CSS
st.markdown(display_window_css, unsafe_allow_html=True)

styles.apply()

user_lat, user_lon = location.get_geolocation()
#st.write(user_lat, user_lon)


# ======= PULLING DATA FROM DATABASE =======
def pull_db():
    if st.session_state.page != "map":
        print("Fetching db...")
        conn = sqlite3.connect('database/map_posts.db')
        # Return in dictionary format
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        cursor.execute(f"SELECT id, latitude, longitude, name, owner FROM map_posts ORDER BY timestamp DESC")
        posts = cursor.fetchall()

        st.session_state.locations = []
        for post in posts:
            st.session_state.locations.append({
                "name": post["name"],
                "lat": post["latitude"],
                "lon": post["longitude"],
                "tag": post["id"],
                "owner": post["owner"]
            })
        

# ======= INITALIZE AND RENDER MAP =======

def initialize_map():
    st.session_state.page = Path(__file__).name.replace('.py', '')
    print(f"Device connected! {datetime.now():%Y-%m-%d %H:%M:%S} - IP: {get_ip.pull_ip()} - {st.session_state.page}")

    # API key: YOUR_STADIA_MAPS_API_KEY
    # Initialize the map at the average location
    style_name = "CartoDB Voyager" 
    tiles_url = f"tiles.stadiamaps.com{style_name}/{{z}}/{{x}}/{{y}}{{r}}.png?api_key=YOUR_STADIA_MAPS_API_KEY"

    #m = folium.Map(location=[user_lat, user_lon], zoom_start=12, tiles=tiles_url, attr='&copy; <a href="https://stadiamaps.com/">Stadia Maps</a>') # Attribution is required)
    m = folium.Map(location=[user_lat, user_lon], zoom_start=12, tiles="CartoDB Voyager", attr='&copy; <a href="https://stadiamaps.com/">Stadia Maps</a>') # Attribution is required)

    css = """
    <style>
    /* This hides the white bubble */
    .leaflet-popup-content-wrapper {
        display: none !important;
    }
    /* This hides the little triangle tip */
    .leaflet-popup-tip-container {
        display: none !important;
    }
    </style>
    """
    m.get_root().header.add_child(folium.Element(css))
    
    return m

def add_user_marker(m, lat, lon):
# Creating user marker
    folium.CircleMarker(
        [lat, lon],
        tooltip="You are here!",
        radius=10,
        color="red",
        fill=True,
        fill_color="#ff6040",
        fill_opacity=0.6
    ).add_to(m)
    
    return m

def read_data(map_data):
    if map_data:
        #print(map_data["last_object_clicked_popup"])
        if st.session_state["last_id"] != map_data["last_object_clicked_popup"]:
            st.session_state.display_window = True
            st.button("✖", on_click=toggle_display_window, type="primary")
                #✖
        else:
            st.session_state.display_window = False
        
        st.session_state["last_id"] = map_data["last_object_clicked_popup"]
        return map_data["last_object_clicked_tooltip"], map_data["last_object_clicked_popup"]
    # Check if user clicked somewhere on the map


# ======= MAP AND LOGIC =======
pull_db()
m = initialize_map()
m = add_user_marker(m, user_lat, user_lon)


# Add markers with popups
for loc in st.session_state.locations:
    
    if loc["owner"] == st.session_state["username"]:
        color = "orange"
    else:
        color = "blue"
    
    folium.Marker(
        [loc["lat"], loc["lon"]],
        tooltip=loc["name"],
        popup=loc["tag"],
        icon=folium.Icon(color=color, icon="circle", prefix="fa")
    ).add_to(m)

# Display map in Streamlit and capture clicks
map_data = st_folium(m, height=1000, use_container_width=True)

name, id = read_data(map_data)

display_window_html = f"""
<div id="display_window" class="{ 'open' if st.session_state.display_window else '' }">

  <h2>{name}</h2>
  <p>Tag ID: {id}</p>
</div>

"""
st.markdown(display_window_html, unsafe_allow_html=True)