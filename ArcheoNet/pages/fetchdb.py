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


if 'lenght' not in st.session_state:
    st.session_state.lenght = 1
    
if "page" not in st.session_state:
    st.session_state.page = "fetchdb"

if st.session_state.page != "fetchdb":
    st.session_state.lenght = 3

st.session_state.page = Path(__file__).name.replace('.py', '')
print(f"Device connected! {datetime.now():%Y-%m-%d %H:%M:%S} - IP: {get_ip.pull_ip()} - {st.session_state.page}")

try:
	username = (st.session_state['userID'])
except:
	st.switch_page("login.py")
if st.session_state["userID"] == None or st.session_state["userID"] == "":
	st.switch_page("login.py")
 
st.set_page_config(
    page_title="ArcheoNet DEV VERSION (alpaha) Login",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

styles.apply()

# ======= Database stuff =======
conn = sqlite3.connect('database/map_posts.db')
# Return in dictionary format
conn.row_factory = sqlite3.Row

cursor = conn.cursor()

def fetch_db():
    # FILTERS
    lat_values = st.slider("Latitude:", 498295972, 498375733, (498295972, 498375733), step=1, format="%.1f")
    lat_min = 0.0000001 * lat_values[0]
    lat_max = 0.0000001 * lat_values[1]
    st.write(lat_min, lat_max)

    # DB and displaying posts
    cursor.execute(f"SELECT * FROM map_posts WHERE latitude BETWEEN ? AND ? ORDER BY timestamp DESC LIMIT {st.session_state.lenght}", (lat_min, lat_max))
    posts = cursor.fetchall()
    print(posts)
    if not posts:
        st.write("No posts found in the database.")
        return
    
    for post in posts:
        col1, col2 = st.columns([1, 3])
        with col1:
            st.header(f"{post['name']}")
            st.write(f"Description: {post['description']}")
            st.write(f"Location: ({post['latitude']}, {post['longitude']})")
            st.write(f"Owner: {post['owner']}")
            st.write(f"Timestamp: {post['timestamp']}")
            st.write(f"ID: {post['id']}")
            st.write("--------------")
        with col2:
            image = post['image']
            st.image(image, width=400)

    if st.button("Fetch more"):
        st.session_state.lenght = st.session_state.lenght + 2
        st.rerun()
    

fetch_db()
